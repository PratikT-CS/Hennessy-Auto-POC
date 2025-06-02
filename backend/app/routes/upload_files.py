from fastapi import APIRouter, UploadFile, File, Path
from fastapi.responses import JSONResponse
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..aws.upload_files_to_s3 import upload_files_to_s3
from ..aws.invoke_bda_job import invoke_bda_job
from ..aws.get_invocation_result import get_invocation_result
from ..aws.get_result_from_s3 import read_json_result_from_s3
from ..crud.deal_crud import create_deal
from ..crud.deal_crud import add_document
from ..db.database import get_db
from app.models.models import DealType, DocumentType
from dotenv import load_dotenv
from ..routes.ws import connections
import os
import json

load_dotenv()
 
router = APIRouter(prefix="/api")

async def infer_document_type(file_name: str) -> DocumentType:
    file_name_lower = file_name.lower()

    if "bill" in file_name_lower or "bos" in file_name_lower:
        return DocumentType.bill_of_sale
    elif "mv1" in file_name_lower:
        return DocumentType.mv1
    elif "dl" in file_name_lower:
        return DocumentType.dl
    elif "title" in file_name_lower:
        return DocumentType.title
    elif "poa" in file_name_lower:
        return DocumentType.poa
    else:
        raise ValueError(f"Cannot infer document type from filename: {file_name}")
 
async def notify(client_id: str, message: str, processing_details: dict):
    """
    Helper function to send a notification to the client via WebSocket.
   
    :param client_id: The ID of the client to notify.
    :param message: The message to send.
    """
    print("Client ID: "+client_id)
    if client_id in connections:
        await connections[client_id].send_json({
            "message": message,
            "processing_started": True,
            "processing_details": processing_details,
            "client_id": client_id
        })
 
def cascade_fail(status_dict):
    keys = ["upload_to_s3", "bda_invocation", "database_update", "validation"]
    for i, key in enumerate(keys):
        if status_dict[key] is False:
            # Modify in place: set all following steps to False
            for next_key in keys[i + 1:]:
                status_dict[next_key] = False
            break
 
@router.post("/upload/{client_id}/{deal_id}", tags=["Upload Files"])
async def upload_and_process_files(
    client_id: str = Path(..., description="Client ID for WebSocket connection"),
    deal_id: str = Path(..., description="Deal ID for the files being uploaded"),
    files: list[UploadFile] = File(..., description="List of files to upload"),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to upload files to S3.
   
    :param deal_id: Query parameter given in the API query parameters.
    :param files: List of files to be uploaded.
    """
    bucket_name = os.getenv("S3_BUCEKT_NAME")
    print("Bucket name upload files: "+bucket_name)
    final_response = {}
    processing_details = {
        "deal_id": deal_id,
        "documents_details":{}
    }
    deal = await create_deal(db=db, frontend_deal_id=deal_id, deal_type=DealType.tag_and_title)

    try:
        for file in files:
            file_content = await file.read()
            await file.seek(0)
            file_name = file.filename
            final_response[file_name] = {}
            processing_details['documents_details'][file_name] = {
                "upload_to_s3": None,
                "bda_invocation": None,
                "database_update": None,
                "validation": None
            }
 
            await notify(client_id, f"Uploading file {file_name} for deal {deal_id} to S3.", processing_details)
           
            response = upload_files_to_s3(
                file_content=file_content,
                file_name=file_name,
                deal_id=deal_id
            )
           
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                final_response[file_name].update({"upload_to_s3": False})
                processing_details['documents_details']['file_name'].update({"upload_to_s3": False})
                await notify(client_id, f"Error uploading file {file_name} to S3", processing_details)
                cascade_fail(processing_details['documents_details'][file_name])
                continue
               
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                final_response[file_name].update({"upload_to_s3": True})
                processing_details['documents_details'][file_name].update({"upload_to_s3": True})
                await notify(client_id, f"File {file_name} uploaded to S3 successfully", processing_details)
               
                result = invoke_bda_job(f"s3://{bucket_name}/input/{deal_id}/{file_name}", f"s3://{bucket_name}/output/{deal_id}")
               
                await notify(client_id, f"BDA invocation started for file {file_name}, invocationARN: {result['invocationArn']}", processing_details)
               
                invocation_arn = result['invocationArn']
                status = get_invocation_result(invocation_arn)
                extracted_data = {}
 
                if status.get('status') == "Success":
                    final_response[file_name].update({"bda_invocation": True})
                    processing_details['documents_details'][file_name].update({"bda_invocation": True})
                    result_url = status['outputConfiguration']['s3Uri']
                    extracted_data = await read_json_result_from_s3(result_url)
                    await notify(client_id, f"BDA invocation completed for file {file_name} successfully. Results are stored in {status.get('outputConfiguration')['s3Uri'].replace('job_metadata.json', '0/custom_output/0/result.json')}", processing_details)
                else:
                    final_response[file_name].update({"bda_invocation": False})
                    processing_details['documents_details'][file_name].update({"bda_invocation": False})
                    await notify(client_id, f"BDA invocation completed with error for file {file_name}. Error: {status}", processing_details)
                    cascade_fail(processing_details['documents_details'][file_name])
                    continue
                
                document_type = await infer_document_type(file_name)

                try:
                    await add_document(
                        db=db,
                        deal_id=deal.id,
                        document_type=document_type,
                        s3_url=f"s3://{bucket_name}/input/{deal_id}/{file_name}",
                        extracted_data=extracted_data,
                    )
                    final_response[file_name].update({"database_update": True})
                    processing_details['documents_details'][file_name].update({"database_update": True})
                    await notify(client_id, f"Document stored in database successfully for file {file_name}.", processing_details)

                except Exception as e:
                    final_response[file_name].update({"database_update": False})
                    processing_details['documents_details'][file_name].update({"database_update": False})
                    await notify(client_id, f"Failed to store document in database for file {file_name}. Error: {str(e)}", processing_details)
                    cascade_fail(processing_details['documents_details'][file_name])
                    continue
            cascade_fail(processing_details['documents_details'][file_name])
            final_response[file_name].update(processing_details['documents_details'][file_name])
        return {
            "status": json.dumps(final_response)
        }
    except Exception as e:
        print(f"Error uploading files: {e}")
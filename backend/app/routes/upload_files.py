from fastapi import APIRouter, UploadFile, File, Path
from fastapi.responses import JSONResponse
from ..aws.upload_files_to_s3 import upload_files_to_s3
from ..aws.invoke_bda_job import invoke_bda_job
from ..aws.get_invocation_result import get_invocation_result
from dotenv import load_dotenv
from ..routes.ws import connections
import os
import json

load_dotenv()

router = APIRouter(prefix="/api")

async def notify(client_id: str, message: str):
    """
    Helper function to send a notification to the client via WebSocket.
    
    :param client_id: The ID of the client to notify.
    :param message: The message to send.
    """
    print("Client ID: "+client_id)
    if client_id in connections:
        await connections[client_id].send_text(message)

@router.post("/upload/{client_id}/{deal_id}", tags=["Upload Files"])
async def upload_and_process_files(
    client_id: str = Path(..., description="Client ID for WebSocket connection"),
    deal_id: str = Path(..., description="Deal ID for the files being uploaded"),
    files: list[UploadFile] = File(..., description="List of files to upload")
):
    """
    Endpoint to upload files to S3. 
    
    :param deal_id: Query parameter given in the API query parameters.
    :param files: List of files to be uploaded.
    """ 
    bucket_name = os.getenv("S3_BUCEKT_NAME")
    print("Bucket name upload files: "+bucket_name)
    final_response = {}
    try:
        for file in files:
            file_content = await file.read()
            await file.seek(0)
            file_name = file.filename
            final_response[file_name] = {}

            await notify(client_id, f"Uploading file {file_name} for deal {deal_id} to S3.")
            
            response = upload_files_to_s3(
                file_content=file_content, 
                file_name=file_name, 
                deal_id=deal_id
            )
            
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                await notify(client_id, f"Error uploading file {file_name} to S3")
                final_response[file_name].update({"upload_to_s3": False})
                
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                final_response[file_name].update({"upload_to_s3": True})
                await notify(client_id, f"File {file_name} uploaded to S3 successfully")
                # await notify(client_id, f"Invoking BDA job for file {file_name}")
                
                result = invoke_bda_job(f"s3://{bucket_name}/input/{deal_id}/{file_name}", f"s3://{bucket_name}/output/{deal_id}")
                
                await notify(client_id, f"BDA invocation started for file {file_name}, invocationARN: {result['invocationArn']} ")
                
                invocation_arn = result['invocationArn']
                status = get_invocation_result(invocation_arn)

                if status.get('status') == "Success":
                    final_response[file_name].update({"bda_invocation": True})
                    await notify(client_id, f"BDA invocation completed for file {file_name} successfully. Results are stored in {status.get('outputConfiguration')['s3Uri'].replace('job_metadata.json', '0/custom_output/0/result.json')}")
                else:
                    final_response[file_name].update({"bda_invocation": False})
                    await notify(client_id, f"BDA invocation completed with error for file {file_name}. Error: {status}")
                
        return {
            "status": json.dumps(final_response)
        }
    except Exception as e:
        print(f"Error uploading files: {e}")
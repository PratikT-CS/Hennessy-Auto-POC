from fastapi import APIRouter, Query, UploadFile, File
from fastapi.responses import JSONResponse
from ..aws.upload_files_to_s3 import upload_files_to_s3
from ..aws.invoke_bda_job import invoke_bda_job
from ..aws.get_invocation_result import get_invocation_result
from dotenv import load_dotenv
from ..routes.ws import connections
import os

load_dotenv()

router = APIRouter(prefix="/api")

@router.get("/upload", tags=["Upload Files"])
async def upload_and_process_files(
    client_id: str,
    deal_id = Query(..., description="Deal ID to associate with the files"),
    files: list[UploadFile] = File(..., description="List of files to upload")
    ):
    """
    Endpoint to upload files to S3. 
    
    :param deal_id: Query parameter given in the API query parameters.
    :param files: List of files to be uploaded.
    """ 
    bucket_name = os.getenv("S3_BUCKET_NAME")
    
    try:
        for file in files:
            if client_id in connections:
                await connections[client_id].send_text(f"Uploading file {file.filename} to S3")
            
            file_content = await file.file.read()
            await file.seek(0)
            file_name = file.filename
            
            # Call the upload function (assuming it's defined elsewhere)
            response = await upload_files_to_s3(file_content=file_content, file_name=file_name, deal_id=deal_id)
            
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                if client_id in connections:
                    await connections[client_id].send_text(f"Error uploading file {file_name} to S3")
                raise Exception(f"Failed to upload file {file_name} to S3")
                
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                if client_id in connections:
                    await connections[client_id].send_text(f"File {file_name} uploaded to S3 successfully")
                    await connections[client_id].send_text(f"Invoking BDA job for file {file_name}")
                    
                    result = invoke_bda_job("s3://{bucket_name}/{deal_id}/{file_name}", "s3://{bucket_name}/output/{deal_id}/")
                    
                    await connections[client_id].send_text(f"BDA invocation started for file {file_name}, invocationARN: {result['invocationArn']} ")
                    
                    invocation_arn = result['invocationArn']
                    status = get_invocation_result(invocation_arn)

                    if status.get('status') == "Success":
                        await connections[client_id].send_text(f"BDA invocation completed for file {file_name} successfully. Results are stored in {status.outputConfiguration['s3Uri'].replace('job_metadata.json', '0/custom_output/0/result.json')}")
                    else:
                        await connections[client_id].send_text(f"BDA invocation completed with error for file {file_name}. Error: {status}")
                
        return {
            status: "Uploading"
        }
    except Exception as e:
        print(f"Error uploading files: {e}")
        return JSONResponse(status_code=500, content={"message": f"Error uploading files: {str(e)}"})
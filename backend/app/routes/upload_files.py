from fastapi import APIRouter, Query, UploadFile, File
from aws.upload_files_to_s3 import upload_files_to_s3
from aws.invoke_bda_job import invoke_bda_job
import os

router = APIRouter(prefix="/api")

@router.get("/upload", tags=["Upload Files"])
async def upload_and_process_files(
    deal_id = Query(..., description="Deal ID to associate with the files"), 
    files: list[UploadFile] = File(..., description="List of files to upload")
    ):
    """
    Endpoint to upload files to S3.
    """
    bucket_name = os.getenv("S3_BUCKET_NAME")
    try:
        for file in files:
            file_content = file.file.read()
            file_name = file.filename
            
            # Call the upload function (assuming it's defined elsewhere)
            response = await upload_files_to_s3(file_content=file_content, file_name=file_name, deal_id=deal_id)
            
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                return {
                    'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
                    'body': f"Error uploading file {file_name} to S3"
                }
                
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print("Bedrock Data Automation Job Started")
                result = invoke_bda_job("s3://{bucket_name}/{deal_id}/{file_name}", "s3://{bucket_name}/output/")
                
                
    except Exception as e:
        print(f"Error uploading files: {e}")
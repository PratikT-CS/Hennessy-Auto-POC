import boto3
import json
import os

from dotenv import load_dotenv
load_dotenv()

def upload_files_to_s3(file_content, file_name, deal_id):
    """
    Function to upload files to S3.
    
    :param file_content: Content of the file to be uploaded
    :param file_name: Name of the file to be uploaded
    :param deal_id: Deal ID to associate with the file
    :return: Response from S3 upload
    """
    try:
        s3_client = boto3.client('s3')
        
        bucket_name = os.getenv('S3_BUCEKT_NAME')
        print(bucket_name)
        s3_key = f'input/{deal_id}/{file_name}'
        
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=file_content
        )
        
        return response
    
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        raise e

if __name__ == "__main__":
    upload_files_to_s3(json.dumps({"sdas":123}), "test.json", "12345")
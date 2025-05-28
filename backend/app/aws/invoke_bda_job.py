import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def invoke_bda_job(s3uri, s3uri_output):
    """
    Function for invoking BDA (Bedrock Data Automation) job.


    """
    bda_runtime_client = boto3.client("bedrock-data-automation-runtime")

    response = bda_runtime_client.invoke_data_automation_async(
        inputConfiguration={
            's3Uri': s3uri
        },
        outputConfiguration={
            's3Uri': s3uri_output
        },
        dataAutomationConfiguration= { 
        "dataAutomationProjectArn": os.getenv('DATA_AUTOMATION_PROJECT_ARN'),
            "stage": "LIVE"
        },
        dataAutomationProfileArn=os.getenv('DATA_AUTOMATION_PROFILE_ARN')
    )
    
    print(response)
    
if __name__ == "__main__":
    invoke_bda_job("s3://hennessy-auto-poc/input/MV1.pdf", "s3://hennessy-auto-poc/output/mv1-test")
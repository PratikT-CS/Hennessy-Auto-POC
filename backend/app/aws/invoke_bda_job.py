import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def invoke_bda_job(s3uri, s3uri_output):
    """
    Function for invoking BDA (Bedrock Data Automation) job.

    :param s3uri: S3 URI of the input file
    :param s3uri_output: S3 URI for the output file
    :return: Response from the BDA job invocation
    """
    bda_runtime_client = boto3.client("bedrock-data-automation-runtime")
    print(f"s3Uri input: {s3uri}")
    print(f"s3Uri output: {s3uri_output}")
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
    return response
    
if __name__ == "__main__":
    invoke_bda_job("s3://hennessy-auto-poc/input/MV1.pdf", "s3://hennessy-auto-poc/output/mv1-test")
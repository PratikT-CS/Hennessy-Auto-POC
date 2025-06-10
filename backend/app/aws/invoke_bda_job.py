import boto3
import os
from dotenv import load_dotenv
from ..aws.session import create_session
from ..aws.blueprints import blueprints

load_dotenv()

def filter_bluerprint(s3Uri):
    """
    Function to filter blueprint based on the S3 URI.

    :param s3uri: S3 URI of the input file
    :return: Filtered blueprint list
    """
    file_name = s3Uri.lower()

    as_of_now_files = ["bill of sale", "compliance pack", "mv-1", "store pack"]

    for name in as_of_now_files:
        if name in file_name:
            return blueprints[name]
    
    return blueprints

def invoke_bda_job(s3uri, s3uri_output):
    """
    Function for invoking BDA (Bedrock Data Automation) job.

    :param s3uri: S3 URI of the input file
    :param s3uri_output: S3 URI for the output file
    :return: Response from the BDA job invocation
    """
    session = create_session()
    bda_runtime_client = session.client("bedrock-data-automation-runtime")

    # filter blueprint from file name
    blueptints = filter_bluerprint(s3uri)

    # logging s3uris and bluprints arns
    print(f"#######################################")
    print(f"Input S3 URI: {s3uri}")
    print(f"Output S3 URI: {s3uri_output}")
    print(f"Blurprint ARN S3 URI: {s3uri}")

    # invoke bda with filtered blueprint
    response = bda_runtime_client.invoke_data_automation_async(
        blueprints=[blueptints],
        inputConfiguration={
            "s3Uri": s3uri,
        },
        outputConfiguration={
            "s3Uri": s3uri_output,
        },
        dataAutomationProfileArn=os.getenv('DATA_AUTOMATION_PROFILE_ARN')
    )

    # return reponse
    print(response)
    print(f"#######################################")
    return response
    
if __name__ == "__main__":
    invoke_bda_job("s3://idppochennessyauto-replica1/Documents/1_1/198049/198049_GA MV-1 (06_20).pdf", "s3://bedrock-bda-us-east-1-457f0017-3669-45e3-aa34-5db2029fc5c6/output/merged_test/198049/")
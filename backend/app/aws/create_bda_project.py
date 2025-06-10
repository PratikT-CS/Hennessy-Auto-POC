import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv()

def create_bda_project():
    """
    Function to create a BDA project.

    :return: Response from the BDA project creation
    """
    session = boto3.session.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=os.getenv("AWS_REGION_NAME")
    )
    bda_client = session.client(
        "bedrock-data-automation"
    )

    blueprints = [
        {
            "blueprintArn": "arn:aws:bedrock:us-east-1:727308806476:blueprint/27f6ca9f2e34",
            "blueprintStage": "LIVE"
        },
        {
            "blueprintArn": "arn:aws:bedrock:us-east-1:727308806476:blueprint/d54b621e8fde",
            "blueprintStage": "LIVE"
        }
    ]

    output_config = {
        'document': {
            'extraction': {
                'granularity': {'types': ['DOCUMENT', 'PAGE']},
                'boundingBox': {'state': 'ENABLED'}
            },
            'generativeField': {'state': 'ENABLED'},
            'outputFormat': {
                'textFormat': {'types': ['MARKDOWN']},
                'additionalFileFormat': {'state': 'ENABLED'}
            }
        }
    }
    bda_client = boto3.client("bedrock-data-automation")
    response = bda_client.create_data_automation_project(
        projectName= "hennessy-test",
        projectDescription="BDA Project For IDP Solution for Car Dealerships",
        projectStage='LIVE',
        standardOutputConfiguration=output_config,
        customOutputConfiguration={
            'blueprints': blueprints 
        },
        overrideConfiguration={'document': {'splitter': {'state': 'ENABLED'}}}
    )
  
    print(response)
    return response

if __name__ == "__main__":
    print("Creating BDA project...")
    create_bda_project()
    print("BDA project created.")
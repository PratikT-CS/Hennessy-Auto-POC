import json
import time
from ..aws.session import create_session

def get_invocation_result(invocation_arn):
    """
    Function to get the result of a BDA job invocation.
    
    :param invocation_arn: ARN of the BDA job invocation
    :return: Result of the BDA job invocation
    """
    session = create_session()
    bda_runtime_client = session.client("bedrock-data-automation-runtime")
    
    print(f"#####################################")
    print(f"Waiting for invocation result: ")

    while True:
        response = bda_runtime_client.get_data_automation_status(
            invocationArn=invocation_arn
        )
        status = response.get("status")
        
        if status in ["Success", "ServiceError", "ClientError", "Failed"]:
            break
        
        time.sleep(8)
    print(f"Result: {response}")
    print(f"#####################################")
    return response

if __name__ == "__main__":
    # Example invocation ARN for testing
    example_invocation_arn = "arn:aws:bedrock:us-east-1:727308806476:data-automation-invocation/a17279b0-5b03-4920-81e9-7e3485f84563"
    result = get_invocation_result(example_invocation_arn)
    print(json.dumps(result, indent=4))
import boto3
import json
import time

def get_invocation_result(invocation_arn):
    """
    Function to get the result of a BDA job invocation.
    
    :param invocation_arn: ARN of the BDA job invocation
    :return: Result of the BDA job invocation
    """
    bda_runtime_client = boto3.client("bedrock-data-automation-runtime")
    
    while True:
        response = bda_runtime_client.get_data_automation_status(
            invocationArn=invocation_arn
        )
        status = response.get("status")
        
        if status in ["Success", "ServiceError", "ClientError", "Failed"]:
            break
        
        time.sleep(8)
    print(response)
    return response

if __name__ == "__main__":
    # Example invocation ARN for testing
    example_invocation_arn = "arn:aws:bedrock:us-east-1:970547377074:data-automation-invocation/dc5f093c-7c53-4a3a-a294-35267b428bd1"
    result = get_invocation_result(example_invocation_arn)
    print(json.dumps(result, indent=4))
import boto3
import json
from urllib.parse import urlparse
import anyio

async def read_json_result_from_s3(s3_url: str):
    def _read_json():
        trimmed_url = s3_url.rsplit('/', 1)[0]
        url = trimmed_url + "/0/custom_output/0/result.json"
        parsed_url = urlparse(url)
        bucket = parsed_url.netloc
        key = parsed_url.path.lstrip('/')

        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        json_data = json.loads(content)
        return json_data["inference_result"]

    return await anyio.to_thread.run_sync(_read_json)

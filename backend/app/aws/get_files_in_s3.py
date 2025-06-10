from urllib.parse import urlparse
from ..aws.session import create_session

def list_files_in_s3_uri(s3_uri: str):
    """
    List all files in the given S3 URI.

    :param s3_uri: The S3 URI (e.g., s3://my-bucket/path/to/folder/)
    :return: List of full S3 keys
    """
    parsed = urlparse(s3_uri)
    bucket = parsed.netloc
    prefix = parsed.path.lstrip("/")

    session = create_session()
    s3 = session.client("s3")

    files = []
    continuation_token = None
    
    print(f"#####################################")
    print(f"Fetching file names from S3")

    while True:
        list_kwargs = {
            "Bucket": bucket,
            "Prefix": prefix,
        }
        if continuation_token:
            list_kwargs["ContinuationToken"] = continuation_token

        response = s3.list_objects_v2(**list_kwargs)

        contents = response.get("Contents", [])
        for obj in contents:
            files.append(obj["Key"])

        if response.get("IsTruncated"):
            continuation_token = response["NextContinuationToken"]
        else:
            break

    print(f"Fetched files names from S3")
    print(f"#####################################")
    return files

if __name__ == "__main__":
    print("Started!")
    files = list_files_in_s3_uri("s3://idppochennessyauto-replica1/Documents/1_1/198695/")
    for file in files:
        print(file)
    print("Finished!")
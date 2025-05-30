import boto3

def generate_presigned_url(s3Uri):
    """
    Generate a presigned URL for an S3 object.
    :param str: S3 uri for the object
    :return: Presigned URL as a string
    """
    s3 = boto3.client('s3')

    parts = s3Uri.split('/',3)
    bucket_name = parts[-2]
    object_key = parts[-1]

    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key, "ResponseContentDisposition": "inline"},
        ExpiresIn=300  # expiration in seconds
    )   

    print(f"Presigned URL: {presigned_url}")
    return presigned_url

if __name__ == "__main__":
    print("Start")
    generate_presigned_url("s3://hennessy-auto-poc/input/250001/BOS.pdf")
    print("End")
import boto3

def create_session():
    try:
        session = boto3.session.Session(
            profile_name="bedrock-dev-karan-hennessy"
        )
        return session
    except Exception as e :
        print(f"error in create session {e}")
        raise e
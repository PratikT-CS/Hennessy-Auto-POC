from fastapi import APIRouter, UploadFile, File, Path
from fastapi.responses import JSONResponse
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..aws.upload_files_to_s3 import upload_files_to_s3
from ..aws.invoke_bda_job import invoke_bda_job
from ..aws.get_invocation_result import get_invocation_result
from ..aws.get_result_from_s3 import read_json_result_from_s3
from ..crud.deal_crud import create_deal
from ..crud.deal_crud import add_document
from ..db.database import get_db
from app.models.models import DealType, DocumentType
from dotenv import load_dotenv
from ..routes.ws import connections
import os
import json
from pydantic import BaseModel
from ..aws.get_files_in_s3 import list_files_in_s3_uri

load_dotenv()

class Item(BaseModel):
    deal_s3Uri: str
    client_id: str
    deal_id: str

router = APIRouter(prefix="/api", tags=["process"])

@router.post("process")
async def process_files(
    item: Item
):
    # Get files for deal from S3 using S3Uri
    files = list_files_in_s3_uri(item.deal_s3Uri)

    # Invoke BDA for files for our use case as of now, in future for all files
    s3_output_uri = f"s3://{os.getenv('S3_OUTPUT_BUCEKT_NAME')}/output-terminal/{item.deal_id}/"

    invocation_arns = []
    files_to_process_as_of_now = ["bill of sale", "compliance pack", "mv-1", "store pack"]
    for file in files:
        for name in files_to_process_as_of_now:
            if name in file.lower():
                response = invoke_bda_job(file, s3_output_uri)
                invocation_arns.append(response['invocationArn'])

    # Wait for each file to process
    invocation_results = []

    while len(invocation_results) != len(invocation_arns):
        for invocation_arn in invocation_arns:
            response = get_invocation_result(invocation_arn)
            if response is not None:
                invocation_results.append(response)

    return {"Status": f"Processing complete"}
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from ..aws.generate_presigned_url import generate_presigned_get_url

router = APIRouter(prefix="/api")

class Item(BaseModel):
    s3Uri: str

@router.get("/presigned-url/{s3Uri}", tags=["S3"])
def get_presigned_url(
    item: Item
):
    """
    Returns a presigned URL for viewing an S3 file.
    """
    s3Uri = Item.s3Uri
    url = generate_presigned_get_url(s3Uri)

    if not url:
        raise HTTPException(status_code=500, detail="Failed to generate presigned URL.")

    return {"url": url}
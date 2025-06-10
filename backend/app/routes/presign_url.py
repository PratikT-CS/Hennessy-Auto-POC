from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
# from ..aws.generate_presigned_url import generate_presigned_get_url
from ..aws.generate_presigned_url import generate_presigned_url

router = APIRouter(prefix="/api")

class Item(BaseModel):
    s3Uri: str

@router.get("/presigned_url", tags=["S3"])
def get_presigned_url(
    item: Item
):
    """
    Returns a presigned URL for viewing an S3 file.
    """
    s3Uri = item.s3Uri
    url = generate_presigned_url(s3Uri)

    if not url:
        raise HTTPException(status_code=500, detail="Failed to generate presigned URL.")

    return {"url": url}
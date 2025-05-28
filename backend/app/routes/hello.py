from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Hello"])

@router.get("/")
def say_hello():
    return {"message": "Hello from FastAPI route!"}
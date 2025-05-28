from fastapi import FastAPI
from backend.app.routes import upload_files
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Include routes
app.include_router(upload_files.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Backend!"}
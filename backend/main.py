from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload_files
from app.routes import ws
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # use ["*"] for development if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(upload_files.router)
app.include_router(ws.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Backend!"}
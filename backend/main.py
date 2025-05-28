from fastapi import FastAPI, Depends
from app.routes import hello
from app.db.database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import deal_crud
import logging
import traceback

app = FastAPI()

# Include routes
app.include_router(hello.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Backend!"}

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@app.post("/deals/sample")
async def create_deal(session: AsyncSession = Depends(get_db)):
    deal = await deal_crud.create_sample_deal(session)
    return {"deal_id": deal.id}

@app.get("/deals/{deal_id}")
async def read_deal(deal_id: int, session: AsyncSession = Depends(get_db)):
    deal_details = await deal_crud.get_deal_details(session, deal_id)
    if not deal_details:
        return {"error": "Deal not found"}
    return deal_details
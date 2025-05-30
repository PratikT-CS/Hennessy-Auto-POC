import asyncio
from .database import engine
from app.models.models import Base

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Optional: to start fresh
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())

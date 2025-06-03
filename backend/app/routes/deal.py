from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from datetime import datetime, timedelta
from app.db.database import get_db
from app.models.models import Deal

router = APIRouter(prefix="/api", tags=["Deals"])

@router.get("/deals")
async def get_grouped_deals(session: AsyncSession = Depends(get_db)):
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    yesterday_start = today_start - timedelta(days=1)
    last_7_days_start = today_start - timedelta(days=7)
    last_30_days_start = today_start - timedelta(days=30)

    result = await session.execute(select(Deal))
    deals = result.scalars().all()

    grouped = {
        "Today": [],
        "Yesterday": [],
        "Last 7 Days": [],
        "Previous 30 Days": []
    }

    for deal in deals:
        created = deal.created_at
        frontend_id = deal.frontend_deal_id

        if created >= today_start:
            grouped["Today"].append(frontend_id)
        elif yesterday_start <= created < today_start:
            grouped["Yesterday"].append(frontend_id)
        elif last_7_days_start <= created < yesterday_start:
            grouped["Last 7 Days"].append(frontend_id)
        elif last_30_days_start <= created < last_7_days_start:
            grouped["Previous 30 Days"].append(frontend_id)

    return grouped

@router.get("/deals/{frontend_deal_id}")
async def get_deal_by_frontend_id(frontend_deal_id: str, session: AsyncSession = Depends(get_db)):
    result = await session.execute(
        select(Deal)
        .where(Deal.frontend_deal_id == frontend_deal_id)
        .options(
            selectinload(Deal.persons),
            selectinload(Deal.vehicles),
            selectinload(Deal.documents)
        )
    )
    deal = result.scalars().first()

    if not deal:
        return {"error": "Deal not found"}

    return {
        "deal": {
            "frontendDealId": deal.frontend_deal_id,
            "deal_type": deal.deal_type.value,
            "created_at": deal.created_at.isoformat()
        },
        "documents": [
            {
                "id": str(doc.id),
                "doc_type": doc.document_type.value,
                "s3_url": doc.s3_url,
                "extracted_data": doc.extracted_data
            }
            for doc in deal.documents
        ],
        "persons": [
            {
                "name": person.name,
                "role": person.role.value
            }
            for person in deal.persons
        ],
        "vehicle": (
            {
                "vin": deal.vehicles[0].vin,
                "make": deal.vehicles[0].make,
                "model": deal.vehicles[0].model,
                "year": deal.vehicles[0].year
            } if deal.vehicles else None
        )
    }
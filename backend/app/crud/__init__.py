from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Deal, Person
from sqlalchemy.future import select

async def create_sample_deal(session: AsyncSession):
    deal = Deal(deal_type="tag_and_title", status="processing")

    person = Person(full_name="John Doe", role="buyer")
    deal.people.append(person)

    session.add(deal)
    await session.commit()
    await session.refresh(deal)
    return deal

async def get_all_deals(session: AsyncSession):
    result = await session.execute(select(Deal))
    return result.scalars().all()

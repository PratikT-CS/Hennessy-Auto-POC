from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.models import Deal, DealType, Person, Role, Vehicle, Document, DocumentType


async def create_sample_deal(session: AsyncSession) -> Deal:
    # Create a new Deal
    deal = Deal(deal_type=DealType.tag_and_title)

    # Create Person entries (linked directly to the deal)
    buyer = Person(name="John Doe", role=Role.buyer)
    seller = Person(name="Jane Smith", role=Role.seller)

    # Assign persons to deal
    deal.persons.extend([buyer, seller])

    # Add Vehicle (use list for consistency since it's a one-to-many)
    vehicle = Vehicle(
        vin="1HGCM82633A004352",
        make="Honda",
        model="Accord",
        year=2020
    )
    deal.vehicles.append(vehicle)

    # Add Documents
    deal.documents.extend([
        Document(
            document_type=DocumentType.bill_of_sale,
            s3_url="http://example.com/bill_of_sale.pdf",
            is_validated=True,
            extracted_data={"buyer": "John Doe"}
        ),
        Document(
            document_type=DocumentType.dl,
            s3_url="http://example.com/dl.pdf",
            is_validated=True,
            extracted_data={"name": "John Doe"}
        ),
        Document(
            document_type=DocumentType.mv1,
            s3_url="http://example.com/mv1.pdf",
            is_validated=False,
            extracted_data={}
        )
    ])

    # Persist the deal
    session.add(deal)
    await session.commit()
    await session.refresh(deal)

    return deal


async def get_deal_details(session: AsyncSession, deal_id: int) -> dict | None:
    result = await session.execute(
        select(Deal)
        .where(Deal.id == deal_id)
        .options(
            selectinload(Deal.persons),
            selectinload(Deal.vehicles),
            selectinload(Deal.documents)
        )
    )
    deal = result.scalars().first()
    if not deal:
        return None

    return {
        "id": deal.id,
        "deal_type": deal.deal_type.value,
        "created_at": deal.created_at.isoformat(),
        "vehicles": [
            {
                "vin": v.vin,
                "make": v.make,
                "model": v.model,
                "year": v.year
            }
            for v in deal.vehicles
        ],
        "persons": [
            {
                "name": p.name,
                "role": p.role.value
            }
            for p in deal.persons
        ],
        "documents": [
            {
                "document_type": doc.document_type.value,
                "s3_url": doc.s3_url,
                "is_validated": doc.is_validated,
                "extracted_data": doc.extracted_data
            }
            for doc in deal.documents
        ]
    }

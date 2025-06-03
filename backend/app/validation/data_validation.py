from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.models.models import Document, DocumentType, Person, Vehicle, Role
from ..crud.deal_crud import add_person, add_vehicle
from ..routes.ws import connections
from fastapi import WebSocket
from datetime import datetime

# Helper function to notify frontend (reuse from your API)
async def notify(client_id: str, message: str, processing_details: dict):
    if client_id in connections:
        await connections[client_id].send_json({
            "message": message,
            "processing_started": True,
            "processing_details": processing_details,
            "client_id": client_id
        })

async def process_bill_of_sale(deal_id: int, db: AsyncSession, client_id: str, processing_details: dict):
    """
    Process the bill_of_sale document: extract data and populate persons and vehicles tables.
    """
    # Fetch bill_of_sale document
    result = await db.execute(
        select(Document).where(Document.deal_id == deal_id, Document.document_type == DocumentType.bill_of_sale)
    )
    bos_doc = result.scalars().first()
    if not bos_doc or not bos_doc.extracted_data:
        await notify(client_id, f"No bill_of_sale document found or no extracted data for deal {deal_id}.", processing_details)
        return False

    data = bos_doc.extracted_data

    try:
        # Delete old persons for deal to avoid duplicates
        await db.execute(
            Person.__table__.delete().where(Person.deal_id == deal_id)
        )

        # Add buyer and seller using add_person helper
        await add_person(db, deal_id, data.get("BuyerName"), Role.buyer)
        await add_person(db, deal_id, data.get("SellerName"), Role.seller)

        # Delete old vehicles for deal
        await db.execute(
            Vehicle.__table__.delete().where(Vehicle.deal_id == deal_id)
        )

        # Add vehicle record
        vehicle = Vehicle(
            deal_id=deal_id,
            vin=data.get("VIN"),
            model=data.get("VehicleModel"),
            make=data.get("VehicleManufacturer"),
            year=data.get("VehicleManufactureYear"),
        )
        db.add(vehicle)

        await db.commit()

        await notify(client_id, f"Bill of Sale data processed and persons/vehicles tables populated for deal {deal_id}.", processing_details)

        # Mark bill_of_sale document as validated
        bos_doc.is_validated = True
        await db.commit()

        return True

    except Exception as e:
        await db.rollback()
        await notify(client_id, f"Failed to process Bill of Sale for deal {deal_id}: {str(e)}", processing_details)
        return False



async def validate_poa(deal_id: int, db: AsyncSession, client_id: str, processing_details: dict):
    """
    Validate power_of_attorney document based on persons in the deal.
    Example: Check if applier exists in persons table.
    """
    result = await db.execute(
        select(Document).where(Document.deal_id == deal_id, Document.document_type == DocumentType.poa)
    )
    poa_doc = result.scalars().first()
    if not poa_doc or not poa_doc.extracted_data:
        await notify(client_id, f"No POA document found or no extracted data for deal {deal_id}.", processing_details)
        return False

    data = poa_doc.extracted_data

    try:
        # Check if applier name exists in persons table
        applier_name = data.get("ApplierName")
        print(applier_name)
        # if not applier_name:
        #     await notify(client_id, f"POA document missing 'ApplierName' field for deal {deal_id}.", processing_details)
        #     return False

        # result = await db.execute(
        #     select(Person).where(Person.deal_id == deal_id, Person.name == applier_name, Person.role == Role.applier)
        # )
        # applier = result.scalars().first()

        # if not applier:
        #     await notify(client_id, f"POA validation failed: Applier '{applier_name}' not found in persons table for deal {deal_id}.", processing_details)
        #     return False

        # Mark POA as validated
        poa_doc.is_validated = True
        await db.commit()
        await notify(client_id, f"POA document validated successfully for deal {deal_id}.", processing_details)
        return True

    except Exception as e:
        await db.rollback()
        await notify(client_id, f"POA validation failed for deal {deal_id}: {str(e)}", processing_details)
        return False


async def validate_title(deal_id: int, db: AsyncSession, client_id: str, processing_details: dict):
    """
    Validate title document based on vehicles and persons.
    Example: verify VIN matches a vehicle in deal.
    """
    result = await db.execute(
        select(Document).where(Document.deal_id == deal_id, Document.document_type == DocumentType.title)
    )
    title_doc = result.scalars().first()
    if not title_doc or not title_doc.extracted_data:
        await notify(client_id, f"No Title document found or no extracted data for deal {deal_id}.", processing_details)
        return False

    data = title_doc.extracted_data

    try:
        vin = data.get("VIN")
        print(vin)
        # if not vin:
        #     await notify(client_id, f"Title document missing VIN field for deal {deal_id}.", processing_details)
        #     return False

        # result = await db.execute(
        #     select(Vehicle).where(Vehicle.deal_id == deal_id, Vehicle.vin == vin)
        # )
        # vehicle = result.scalars().first()

        # if not vehicle:
        #     await notify(client_id, f"Title validation failed: VIN '{vin}' not found in vehicles for deal {deal_id}.", processing_details)
        #     return False

        # Mark title as validated
        title_doc.is_validated = True
        await db.commit()
        await notify(client_id, f"Title document validated successfully for deal {deal_id}.", processing_details)
        return True

    except Exception as e:
        await db.rollback()
        await notify(client_id, f"Title validation failed for deal {deal_id}: {str(e)}", processing_details)
        return False


async def validate_mv1(deal_id: int, db: AsyncSession, client_id: str, processing_details: dict):
    """
    Validate driver's license document based on persons.
    Example: verify driver's license name matches buyer or seller.
    """
    result = await db.execute(
        select(Document).where(Document.deal_id == deal_id, Document.document_type == DocumentType.mv1)
    )
    dl_doc = result.scalars().first()
    if not dl_doc or not dl_doc.extracted_data:
        await notify(client_id, f"No Driver's License document found or no extracted data for deal {deal_id}.", processing_details)
        return False

    data = dl_doc.extracted_data

    try:
        dl_name = data.get("DLName")
        print(dl_name)
        # if not dl_name:
        #     await notify(client_id, f"Driver's License document missing DLName field for deal {deal_id}.", processing_details)
        #     return False

        # result = await db.execute(
        #     select(Person).where(Person.deal_id == deal_id, Person.name == dl_name)
        # )
        # person = result.scalars().first()

        # if not person:
        #     await notify(client_id, f"Driver's License validation failed: Name '{dl_name}' not found in persons for deal {deal_id}.", processing_details)
        #     return False

        dl_doc.is_validated = True
        await db.commit()
        await notify(client_id, f"Driver's License document validated successfully for deal {deal_id}.", processing_details)
        return True

    except Exception as e:
        await db.rollback()
        await notify(client_id, f"Driver's License validation failed for deal {deal_id}: {str(e)}", processing_details)
        return False


async def validate_documents_for_deal(deal_id: int, db: AsyncSession, client_id: str, processing_details: dict):
    """
    Main function to validate all documents for a deal in correct order:
    1. Process Bill of Sale (populate persons and vehicles)
    2. Validate POA, Title, DL, and others based on the populated data.
    """
    # 1. Process Bill of Sale first
    bos_valid = await process_bill_of_sale(deal_id, db, client_id, processing_details)
    if not bos_valid:
        await notify(client_id, f"Bill of Sale processing failed for deal {deal_id}. Aborting further validation.", processing_details)
        return False

    # 2. Validate other documents
    poa_valid = await validate_poa(deal_id, db, client_id, processing_details)
    # title_valid = await validate_title(deal_id, db, client_id, processing_details)
    mv1_valid = await validate_mv1(deal_id, db, client_id, processing_details)

    all_valid = all([bos_valid, poa_valid, mv1_valid])

    if all_valid:
        await notify(client_id, f"All documents validated successfully for deal {deal_id}.", processing_details)
    else:
        await notify(client_id, f"Some documents failed validation for deal {deal_id}.", processing_details)

    return all_valid

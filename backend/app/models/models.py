# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean, Text, JSON
# from sqlalchemy.orm import relationship, declarative_base
# from datetime import datetime
# import enum

# Base = declarative_base()

# class DealType(str, enum.Enum):
#     tag_and_title = "tag_and_title"
#     trade_pack = "trade_pack"

# class Role(str, enum.Enum):
#     buyer = "buyer"
#     seller = "seller"
#     owner = "owner"

# class Deal(Base):
#     __tablename__ = "deals"
#     id = Column(Integer, primary_key=True, index=True)
#     deal_type = Column(Enum(DealType), nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     documents = relationship("Document", back_populates="deal")
#     people = relationship("DealPerson", back_populates="deal")
#     vehicle = relationship("Vehicle", uselist=False, back_populates="deal")

# class Document(Base):
#     __tablename__ = "documents"
#     id = Column(Integer, primary_key=True)
#     deal_id = Column(Integer, ForeignKey("deals.id"))
#     document_type = Column(String)  # "bill_of_sale", "mv1", "dl", "title", etc.
#     extracted_data = Column(JSON, nullable=True)
#     file_url = Column(String)
#     is_validated = Column(Boolean, default=False)

#     deal = relationship("Deal", back_populates="documents")

# class Person(Base):
#     __tablename__ = "persons"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     license_number = Column(String, nullable=True)

#     deals = relationship("DealPerson", back_populates="person")

# class DealPerson(Base):
#     __tablename__ = "deal_people"
#     id = Column(Integer, primary_key=True)
#     deal_id = Column(Integer, ForeignKey("deals.id"))
#     person_id = Column(Integer, ForeignKey("persons.id"))
#     role = Column(Enum(Role), nullable=False)

#     deal = relationship("Deal", back_populates="people")
#     person = relationship("Person", back_populates="deals")

# class Vehicle(Base):
#     __tablename__ = "vehicles"
#     id = Column(Integer, primary_key=True)
#     deal_id = Column(Integer, ForeignKey("deals.id"))
#     vin = Column(String, nullable=False)
#     model = Column(String)
#     make = Column(String)
#     year = Column(Integer)

#     deal = relationship("Deal", back_populates="vehicle")

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean, Text, JSON
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class DealType(str, enum.Enum):
    tag_and_title = "tag_and_title"
    trade = "trade"

class DocumentType(str, enum.Enum):
    bill_of_sale = "bill_of_sale"
    mv1 = "mv1"
    dl = "dl"
    title = "title"

class Role(str, enum.Enum):
    buyer = "buyer"
    seller = "seller"
    applier = "applier"

class Deal(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True)
    frontend_deal_id = Column(String, unique=True, nullable=False)
    deal_type = Column(Enum(DealType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    documents = relationship("Document", back_populates="deal", cascade="all, delete-orphan")
    persons = relationship("Person", back_populates="deal", cascade="all, delete-orphan")
    vehicles = relationship("Vehicle", back_populates="deal", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey("deals.id"))
    document_type = Column(Enum(DocumentType))
    s3_url = Column(String)
    extracted_data = Column(JSON, nullable=True)
    is_validated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    deal = relationship("Deal", back_populates="documents")

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey("deals.id"))
    role = Column(Enum(Role), nullable=False)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    deal = relationship("Deal", back_populates="persons")

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey("deals.id"))
    vin = Column(String, nullable=False)
    model = Column(String)
    make = Column(String)
    year = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    deal = relationship("Deal", back_populates="vehicles")

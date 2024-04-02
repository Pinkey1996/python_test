from sqlalchemy import create_engine, Column, Integer, String, Float
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AddressResponse(BaseModel):

    id: int
    name: str
    latitude: float
    longitude: float



class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)


class AddressCreate(BaseModel):
    name: str
    latitude: float
    longitude: float


class AddressUpdate(BaseModel):
    name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

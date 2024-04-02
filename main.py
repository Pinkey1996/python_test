from fastapi import FastAPI, HTTPException, Query, Depends
from geopy.distance import geodesic

from utils.models import Address, AddressCreate, AddressUpdate, AddressResponse
from utils.utils import SessionLocal, get_db


# Set up FastAPI app
app = FastAPI()


@app.post("/addresses/", response_model=AddressResponse)
def create_address(address: AddressCreate, db: SessionLocal = Depends(get_db)):
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


@app.get("/addresses/{address_id}", response_model=AddressResponse)
def read_address(address_id: int, db: SessionLocal = Depends(get_db)):
    address = db.query(Address).filter(Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@app.put("/addresses/{address_id}", response_model=AddressResponse)
def update_address(address_id: int, address: AddressUpdate, db: SessionLocal = Depends(get_db)):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in address.dict().items():
        if value is not None:
            setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address


@app.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: SessionLocal = Depends(get_db)):
    address = db.query(Address).filter(Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    return {"message": "Address deleted successfully"}


# Implement method to retrieve addresses within a given distance and location coordinates
@app.get("/addresses/within_distance/")
def addresses_within_distance(latitude: float, longitude: float, distance: float = Query(...), db: SessionLocal = Depends(get_db)):
    addresses = db.query(Address).all()
    valid_addresses = []
    for address in addresses:
        if geodesic((latitude, longitude), (address.latitude, address.longitude)).meters <= distance:
            valid_addresses.append(address)
    return valid_addresses



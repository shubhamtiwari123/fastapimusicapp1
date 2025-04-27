from fastapi import APIRouter, HTTPException, Depends
from app.models.instrument_model import Instrument, UpdateInstrument
from app.database import db
from app.auth.jwt_bearer import JWTBearer
from bson import ObjectId

router = APIRouter(prefix="/instruments", tags=["instruments"], dependencies=[Depends(JWTBearer())])

collection = db["instruments"]

def instrument_helper(instrument) -> dict:
    return {
        "id": str(instrument["_id"]),
        "name": instrument["name"],
        "type": instrument["type"],
        "brand": instrument["brand"],
        "price": instrument["price"]
    }

@router.post("/")
async def create_instrument(instrument: Instrument):
    new_instrument = await collection.insert_one(instrument.dict())
    created_instrument = await collection.find_one({"_id": new_instrument.inserted_id})
    return instrument_helper(created_instrument)

@router.get("/")
async def get_instruments():
    instruments = []
    async for instrument in collection.find():
        instruments.append(instrument_helper(instrument))
    return instruments

@router.get("/{id}")
async def get_instrument(id: str):
    instrument = await collection.find_one({"_id": ObjectId(id)})
    if instrument:
        return instrument_helper(instrument)
    raise HTTPException(status_code=404, detail="Instrument not found")

@router.put("/{id}")
async def update_instrument(id: str, data: UpdateInstrument):
    instrument = await collection.find_one({"_id": ObjectId(id)})
    if instrument:
        await collection.update_one({"_id": ObjectId(id)}, {"$set": data.dict(exclude_unset=True)})
        updated = await collection.find_one({"_id": ObjectId(id)})
        return instrument_helper(updated)
    raise HTTPException(status_code=404, detail="Instrument not found")

@router.delete("/{id}")
async def delete_instrument(id: str):
    instrument = await collection.find_one({"_id": ObjectId(id)})
    if instrument:
        await collection.delete_one({"_id": ObjectId(id)})
        return {"message": "Instrument deleted successfully"}
    raise HTTPException(status_code=404, detail="Instrument not found")


from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv




load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI is missing. Check your .env file.")


client = AsyncIOMotorClient(MONGO_URI)


db = client["genmgdb"]

genai_data = db["genmgdb-col"]

app=FastAPI()

class genaidata(BaseModel):
    name : str
    phone : int
    city : str
    course : str


class UpdateGenaidata(BaseModel):
    name: str | None = None
    phone: int | None = None
    city: str | None = None
    course: str | None = None

@app.post("/genai/insert")
async def genai_data_insert(data:genaidata):
    result = await genai_data.insert_one(data.dict())
    return str(result.inserted_id)


def mgdb_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


@app.get("/genai/getdata")
async def get_genaimgdb_data():
    iterms = []
    cursor = genai_data.find({})
    async for document in cursor:
          iterms.append(mgdb_helper(document))
    return iterms

@app.put("/genai/update/{id}")
async def update_genai_data(id: str, data: genaidata):
    result = await genai_data.replace_one({"_id": ObjectId(id)}, data.dict())
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"updated_count": result.modified_count}

@app.patch("/genai/partial-update/{id}")
async def partial_update_genai_data(id: str, data: UpdateGenaidata):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    result = await genai_data.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"updated_count": result.modified_count}

@app.delete("/genai/delete/{id}")
async def delete_genai_data(id: str):
    result = await genai_data.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"deleted_count": result.deleted_count}
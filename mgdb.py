from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.encoders import jsonable_encoder
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

@app.post("/genai/insert")
async def genai_data_insert(data:genaidata):
    result = await genai_data.insert_one(data.dict())
    return str(result.inserted_id)

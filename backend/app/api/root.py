from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "connection successful"}
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import root

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",
]

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
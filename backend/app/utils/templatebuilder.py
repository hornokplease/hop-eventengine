import os 
import httpx
import json
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

WABA_ID = os.getenv("WABAID")  
BASE_URL = "https://graph.facebook.com/v16.0"  
ACCESS_TOKEN = os.getenv("ACCESSTOKEN")


class Data(BaseModel): 
    type: Literal["mcq", "scq", "text"]
    question_string: str
    options: list[str] | None = None
    others: bool | None = False

class UserInput(BaseModel):
    data: list[Data]

class FlowRequest(BaseModel):
    name: str
    categories: list[str]


async def create_message_template(flow_id, client_name):
    url = f"{BASE_URL}/{WABA_ID}/message_templates"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "name": f"hopin{client_name.replace(" ", "")}",
        "language": "en_US",
        "category": "MARKETING",
        "components": [
            {
                "type": "body",
                "text": "<text that is sent along with flow>"
            },
            {
                "type": "BUTTONS",
                "buttons": [
                    {
                        "type": "FLOW",
                        "text": "Start Flow!",
                        "navigate_screen": "screen_a",
                        "flow_action": "navigate",
                        "flow_id": flow_id
                    }
                ]
            }
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)



async def publish_flow(flow_id):
    url = f"{BASE_URL}/{flow_id}/publish"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    pass



async def update_flow_json(flow_json, flow_id):
    file_path = Path(__file__).parent / "flow.json"
    with open(file_path, "w") as json_file:
        json.dump(flow_json, json_file)

    url  = f"{BASE_URL}/{flow_id}/assets"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found in the specified directory")
    
    form_data = {
        "name": (None, "flow.json"),
        "asset_type": (None, "FLOW_JSON"),
        "file": (file_path.name, file_path.read_bytes(), "application/json")
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, files=form_data)
        os.remove(file_path)
        if response.status_code == 200:
            return response.json()
        else:  
            raise HTTPException(status_code=response.status_code, detail=response.text)
     
    

async def update_flow_metadata(flow_id: str, updated_flow_name: str):
    url = f"{BASE_URL}/{flow_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {}
    if updated_flow_name:
        data["name"] = updated_flow_name
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)



async def create_flow(flow_request: FlowRequest):
    url = f"{BASE_URL}/{WABA_ID}/flows"   
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "name": flow_request.name,
        "categories": flow_request.categories
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_dict = response.json()
            flow_id = response_dict.get("id") 
            return flow_id        
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
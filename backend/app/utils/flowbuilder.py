from app.utils.flowjson import events_screenbuilder, personalinfo_screenbuilder, additionalinfo_jsonbuilder
from dotenv import load_dotenv
from fastapi import HTTPException
from pathlib import Path
import httpx
import json
import os 

load_dotenv()

WABA_ID = os.getenv("WABAID")  
BASE_URL = "https://graph.facebook.com/v16.0"  
ACCESS_TOKEN = os.getenv("ACCESSTOKEN")

async def create_flow(client_name):
    url = f"{BASE_URL}/{WABA_ID}/flows"   
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "name": client_name,
        "categories": ["SURVEY"]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_dict = response.json()
            flow_id = response_dict.get("id") 
            return flow_id        
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


def flow_builder(client_name, flow_json):
    # creating new flow
    flow_id = create_flow(client_name)
    
    # updating flow meta-data
    if flow_id:
        response_from_update_flow_metadata = update_flow_metadata(flow_id, client_name)
        print(response_from_update_flow_metadata)
    else:
        print("flow metadata couldnt be updated")

    # updating flow json
    if response_from_update_flow_metadata["success"] == True:
        response_from_update_flow_json = update_flow_json(flow_json, flow_id)
        print(response_from_update_flow_json)
    else:
        print("flow json couldnt be updated")

    # publishing the flow
    if flow_id:
        publish_status = publish_flow(flow_id)
        print(publish_status)
    else:
        print("cannot publish flow, as flow_id is invalid")
    
    return flow_id


def process_event_names(front_end_input):
    event_names = [event.event_name for event in front_end_input.events]
    return event_names

def intro_flowbuilder(client_name, front_end_input):
    flow_json = personalinfo_screenbuilder()
    flow_id = flow_builder(client_name, flow_json)
    return flow_id

def events_flowbuilder(client_name, front_end_input):
    event_names = process_event_names(front_end_input)
    flow_json = events_screenbuilder(event_names)
    flow_id = flow_builder(client_name, flow_json)
    return flow_id

def additional_flowbuilder(client_name, front_end_input):
    # @NIKITA 
    # write a logic that creates additionalinfo(AdditionalInfoPydantic from pydantics.py) from db or from 'front_end_input'
    additionalinfo = "test"
    flow_json = additionalinfo_jsonbuilder(additionalinfo)
    flow_id = flow_builder(client_name, flow_json)
    return flow_id
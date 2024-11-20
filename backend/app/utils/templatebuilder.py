from app.utils.flowbuilder import intro_flowbuilder, events_flowbuilder, additional_flowbuilder
from dotenv import load_dotenv
from fastapi import HTTPException
import httpx
import os

load_dotenv()

WABA_ID = os.getenv("WABAID")  
BASE_URL = "https://graph.facebook.com/v16.0"  
ACCESS_TOKEN = os.getenv("ACCESSTOKEN")

async def create_message_template(front_end_input, msg):
    # @NIKITA
    # fetch client name here from the db
    client_name = "test"   # OMIT THIS LINE ONCE FETCHED
    if msg == "intro":
        flow_id = intro_flowbuilder(client_name, front_end_input)
    elif msg == "events":
        flow_id = events_flowbuilder(client_name, front_end_input)
    elif msg == "additional":
        flow_id = additional_flowbuilder(client_name, front_end_input)
        
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
                "text": "<text that is sent along with flow>"  # @NIKITA what sentence should we fill here?
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
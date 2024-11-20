from app.utils.pydantics import FrontendInput
from app.utils.templatebuilder import create_message_template
from dotenv import load_dotenv
from fastapi import APIRouter, Request, Response, HTTPException
import os

load_dotenv()

WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN")

router = APIRouter()


def event_details(front_end_input: FrontendInput):
    events = [{
        "event_name": event.event_name,
        "event_id": event.event_name.replace(" ", "_"),
        "max_attendees": event.max_attendees
    } for event in front_end_input.events
    ]
    return events


@router.get("/")
def read_root():
    return {"message": "connection successful"}

@router.post("/dashboard/event")
async def create_user(request):
    # this function stores info about organizer from frontend into db 
    # and returns an identification token
    pass

@router.post("/dashboard/forms/create")
async def form_creator(frontendinput: FrontendInput):
    events = event_details(frontendinput)
    # @NIKITA 
    # create eventsDB here and store the info from 'events' and 'front_end_input' variable.
    template1 = create_message_template(frontendinput, "intro")
    template2 = create_message_template(frontendinput, "events")
    # @NIKITA
    # store template1 and template2 in a DB
    if template1 and template2:
        return {"template_status": "success"}
    # return client_id or client_name to frontend that can be refetched in /activate
    
@router.post("/dashboard/forms/activate")
async def activate_template(request: Request):
    # fetch client_id from the frontend request
    # fetch name of template 1 & 2 for the respective client_id from db
    # fetch trial phone number from frontend request
    # send template 1 & 2 in order to trial number
    return {"process": "success"}

@router.get("/webhook")
async def verify_webhook(request: Request):
    # Get query parameters from the request
    hub_mode = request.query_params.get("hub.mode")
    hub_challenge = request.query_params.get("hub.challenge")
    hub_verify_token = request.query_params.get("hub.verify_token")

    if hub_mode == "subscribe" and hub_verify_token == WEBHOOK_VERIFY_TOKEN:
        return Response(content=hub_challenge, media_type="text/plain", status_code=200)

    else:
        raise HTTPException(status_code=403, detail="Forbidden")

@router.post("/webhook")
async def post_webhook():
    # FETCH the response_json
    # if response_json == "BIT MANTHAN":
    #         FETCH name of template 1 from db
    #         trigger template 1
    # if response_json == "template 1 response"
    #         STORE required response in db
    #         FETCH name of template 2 from db
    #         trigger template 2
    # if response_json == "template 2 response"
    #         STORE required response in db
    #         CALL ADDITIONAL INFO CREATOR THAT RETURNS TEMPLATE 3 NAME
    #         trigger template 3
    # if response_json == "template 3 response"
    #         STORE required response in db
    #         trigger QR ticket engine
    pass
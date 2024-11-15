from fastapi import APIRouter
from app.utils.pydantics import FrontendInput
from app.utils.flowjson import process_event_names, event, personalinfo_jsonbuilder, event_details_screen_builder

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "connection successful"}

@router.post("/dashboard/forms")
async def form_creator(front_end_input: FrontendInput):
    event_names = process_event_names(front_end_input)
    events = event(front_end_input)
    # create eventsDB here
    flowjson_for_personalinfo = personalinfo_jsonbuilder()
    flowjson_for_events = event_details_screen_builder(event_names)
    return flowjson_for_personalinfo
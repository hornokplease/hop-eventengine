from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class EventDetails(BaseModel):
    event_name : str 
    start_date : str
    end_date : str
    individual_cost: int
    max_cost: int
    max_attendees: int

class FrontendInput(BaseModel):
    events : list[EventDetails]

def payloadbuilder(event_names):
    payload = {}
    for event_name in event_names:
        event_id = event_name.replace(" ", "_")
        event_list = "Event_List"
        event_name_variable = "{form." + event_list + "}"
        payload.update({f"{event_id}" : f"${event_name_variable}"})
    return payload

def mcqbuilder(event_names):
    mcq_element = [
        {
            "type": "TextSubheading",
            "text": "Select the events to attend"
        },
        {
            "type": "CheckboxGroup",
            "label": "minimum: 1",
            "required": True,
            "name": "Event_List",
            "data-source": [
                {
                    "id": event_name.replace(" ", "_"),
                    "title": event_name
                } for event_name in event_names
            ]
                
        },
        {
            "type": "Footer",
            "label": "Submit",
            "on-click-action":{
                "name": "complete",
                "payload": payloadbuilder(event_names)
            },
        }
    ]
    return mcq_element

def event_details_screen_builder(event_names):
    children_of_screen = mcqbuilder(event_names)
    flow_json = {
        "version": "5.0",
        "screens": [
            {
                "id": "screenB",
                "title": "Event Details",
                "data": {},
                "terminal": True,
                "layout": {
                    "type": "SingleColumnLayout",
                    "children": [
                        {
                            "type": "Form",
                            "name": "flow_path",
                            "children": children_of_screen
                        }
                    ]
                }
            }
        ]
    }
    return flow_json

def event(front_end_input: FrontendInput):
    events = [{
        "event_name": event.event_name,
        "event_id": event.event_name.replace(" ", "_"),
        "max_attendees": event.max_attendees
    } for event in front_end_input.events
    ]
    return events

def personalinfo_jsonbuilder():
    flowjson = {
        "version": "5.1",
        "screens": [
          {
            "id": "screenA",
            "title": "Profile Details",
            "data": {},
            "terminal": True,
            "layout": {
              "type": "SingleColumnLayout",
              "children": [
                {
                  "type": "Form",
                  "name": "flow_path",
                  "children": [
                    {
                      "type": "TextSubheading",
                      "text": "Enter your name"
                    },
                    {
                      "type": "TextInput",
                      "label": "name",
                      "name": "Name_Input",
                      "required": True,
                      "input-type": "text"
                    },
                    {
                      "type": "TextSubheading",
                      "text": "Enter your email"
                    },
                    {
                      "type": "TextInput",
                      "label": "example@gmail.com",
                      "name": "Email_Input",
                      "required": True,
                      "input-type": "text"
                    },
                    {
                      "type": "Footer",
                      "label": "Submit",
                      "on-click-action": {
                        "name": "complete",
                        "payload": {
                          "Name": "${form.Name_Input}",
                          "Email": "${form.Email_Input}"
                        }
                      }
                    }
                  ]
                }
              ]
            }
          }
        ]
      }
    return flowjson

def process_event_names(front_end_input: FrontendInput):
    event_names = [event.event_name for event in front_end_input.events]
    return event_names

@app.post("/dashboard/forms")
async def form_creator(front_end_input: FrontendInput):
    event_names = process_event_names(front_end_input)
    events = event(front_end_input)
    # create eventsDB here
    flowjson_for_personalinfo = personalinfo_jsonbuilder()
    flowjson_for_events = event_details_screen_builder(event_names)
    return flowjson_for_personalinfo
from app.utils.pydantics import AdditionalInfoPydantic

ADDITIONALINFO_PAYLOAD_DB = {}
ADDITIONALINFO_DATALOAD_DB = {}

# events form - flowjson builder
def events_payloadbuilder(event_names):
    payload = {}
    for event_name in event_names:
        event_id = event_name.replace(" ", "_")
        event_list = "Event_List"
        event_name_variable = "{form." + event_list + "}"
        payload.update({f"{event_id}" : f"${event_name_variable}"})
    return payload

def events_mcqbuilder(event_names):
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
                "payload": events_payloadbuilder(event_names)
            },
        }
    ]
    return mcq_element

def events_screenbuilder(event_names):
    children_of_screen = events_mcqbuilder(event_names)
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

# personal info form - flowjson builder
def personalinfo_screenbuilder():
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

# additional info form - flowjson builder
def additionalinfo_payload(screen_id, size):
    screen_codes = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"]
    screen_code_plus_one = screen_codes[screen_id + 1]
    if screen_id != (size-1):
        onclickaction = {
            "name": "navigate",
            "next": {
                "type": "screen",
                "name": f"screen_{screen_code_plus_one}"
            }
        }
    else:
        onclickaction = {
            "name": "complete"
        }
    labelform = "${form." + f"dropdown_{screen_id}" + "}"
    payload = {
        f"dropdown_{screen_id}": labelform
    }
    payload.update(ADDITIONALINFO_PAYLOAD_DB)
    onclickaction.update({"payload": payload})
    labeldata = "${data." + f"dropdown_{screen_id}" + "}"
    ADDITIONALINFO_PAYLOAD_DB.update({f"dropdown_{screen_id}": labeldata})
    dataload = {
        f"dropdown_{screen_id}" : {
            "type": "string",
            "__example__": "Example"
        }
    }
    ADDITIONALINFO_DATALOAD_DB.update(dataload)
    return onclickaction

def additionalinfo_children(event_name, max_attendees, screen_id, size):
    upd_max_attendees = max_attendees 
    if screen_id != (size - 1):
        label = "Continue"
    else:
        label = "Submit"
    children = [
        {
            "type": "TextSubheading",
            "text": f"{event_name}"
        },
        {
            "type": "Dropdown",
            "label": "Number of Attendees",
            "required": True,
            "name": f"dropdown_{screen_id}",
            "data-source": [
                {
                    "id": f"{screen_id}_{attendee+1}",
                    "title": f"{attendee+1}"
                }
                for attendee in range(upd_max_attendees)
            ]
        },
        {
            "type": "Footer",
            "label": f"{label}",
            "on-click-action": additionalinfo_payload(screen_id, size)
        }
    ]
    return children

def additionalinfo_screenbuilder(event_name, max_attendees, screen_id, size):
    screen_codes = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"]
    screen_code = screen_codes[screen_id]
    screen = {
        "id": f"screen_{screen_code}",
        "title": f"Event {screen_id + 1}"
    }
    data = {}
    if screen_id != 0:
        data.update(ADDITIONALINFO_DATALOAD_DB)
    layout = {
        "type": "SingleColumnLayout",
        "children": [{
            "type": "Form",
            "name": "flow_path",
            "children": additionalinfo_children(event_name, max_attendees, screen_id, size)
        }]
    }  
    screen.update({"data": data})
    if screen_id == size-1:   
        screen.update({"terminal": True})
    screen.update({"layout": layout})
    return screen

def additionalinfo_jsonbuilder(additionalinfo: AdditionalInfoPydantic):
    flowjson = {
        "version": "5.1",
        "screens": [
            additionalinfo_screenbuilder(infoforevent.event_name, infoforevent.max_attendees, index, len(additionalinfo.events))
            for index, infoforevent in enumerate(additionalinfo.events)
        ]
    }
    return flowjson
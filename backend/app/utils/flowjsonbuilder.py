import json
from pydantic import BaseModel
from typing import Literal


PAYLOAD_DB = {}

ELEMENT_DATA_DB = {}


class question_data(BaseModel):
    type: Literal["mcq", "scq", "text"]
    question_string: str
    options: list[str] | None = None
    others: bool | None = False


def payloadbuilder(screen_code, element_unique_names, question_type):
    payload = {}
    dataload = {}

    for i in range(len(element_unique_names)):
        payload_value_variable = "{form." + element_unique_names[i] + "}"
        payload_key = f"screen_{screen_code}_{element_unique_names[i]}_{screen_code}"
        payload_value = f"${payload_value_variable}"
        payload.update({payload_key:payload_value})

        payload.update(PAYLOAD_DB)

        payload_db_value_variable = "{data." + payload_key + "}"
        payload_db_key = payload_key
        payload_db_value = f"${payload_db_value_variable}"
        PAYLOAD_DB.update({payload_db_key: payload_db_value})

        if question_type == "mcq":
            dataload_value = {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "__example__": []
            }
        elif question_type == "scq":
            dataload_value = {
                "type": "string",
                "__example__": "Example"
            }
        else:
            dataload_value = {
                "type": "string",
                "__example__": "Example"
            }

        dataload.update({payload_key : dataload_value})

    element_data_db_key = screen_code
    element_data_db_value = dataload
    ELEMENT_DATA_DB.update({element_data_db_key: element_data_db_value})

    return {"payload": payload}



def footerbuilder(screen_code, element_unique_names, question_type, size):
    footer = {}
    screen_codes = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"]
    screen_id = screen_codes.index(screen_code)
    
    footerheader = {
        "type": "Footer",
        "label": "Continue",
    }

    if screen_id != size:      
        on_click_action = {
            "name": "navigate",
            "next": {
                "type": "screen",
                "name": f"screen_{screen_codes[screen_id+1]}"
            }
        }
    else:
        on_click_action = {
            "name": "complete"
        }

    payload = payloadbuilder(screen_code, element_unique_names, question_type)

    on_click_action.update(payload)

    footer.update(footerheader)
    footer.update({"on-click-action": on_click_action})

    return footer



def mcqbuilder(screen_code, question: question_data, size):
    question_text = question.question_string
    options = question.options
    others = question.others
    mcq_element = [
        {
            "type": "TextSubheading",
            "text": question_text
        },
        {
            "type": "CheckboxGroup",
            "label": "(Select all that apply)",
            "required": True,
            "name": f"Checkboxgroup_{screen_code}",
            "data-source": [{"id": f"{screen_code}_{options[i]}", "title": options[i]} for i in range(len(options))]
        }
    ]
    element_unique_names = [mcq_element[1]["name"]]

    if others:
        mcq_element.append(
            {
                "type": "TextInput",
                "label": "Others",
                "name": f"TextInput_{screen_code}",
                "required": False,
                "input-type": "text"
            }
        )
        element_unique_names.append(mcq_element[2]["name"])
    footer = footerbuilder(screen_code, element_unique_names, "mcq", size)
    mcq_element.append(footer)
    return mcq_element



def scqbuilder(screen_code, question: question_data, size):
    question_text = question.question_string
    options = question.options
    others = question.others
    scq_element = [
        {
            "type": "TextSubheading",
            "text": question_text
        },
        {
            "type": "RadioButtonsGroup",
            "label": "(Select one option)",
            "required": True,
            "name": f"RadioButtonsgroup_{screen_code}",
            "data-source": [{"id": f"{screen_code}_{options[i]}", "title": options[i]} for i in range(len(options))]
        }
    ]
    element_unique_names = [scq_element[1]["name"]]
    
    if others:
        scq_element.append(
            {
                "type": "TextInput",
                "label": "Others",
                "name": f"TextInput_{screen_code}",
                "required": False,
                "input-type": "text"
            }
        )
        element_unique_names.append(scq_element[2]["name"])
    footer = footerbuilder(screen_code, element_unique_names, "scq", size)
    scq_element.append(footer)
    return scq_element



def textbuilder(screen_code, question: question_data, size):
    question_text = question.question_string
    text_element = [
        {
            "type": "TextSubheading",
            "text": question_text
        },
        {
            "type": "TextArea",
            "label": "Your Answer",
            "required": True,
            "name": f"TextArea_{screen_code}"
        }
    ]
    element_unique_names = [text_element[1]["name"]]
    footer = footerbuilder(screen_code, element_unique_names, "text", size)
    text_element.append(footer)
    return text_element



def screenbuilder(screen_id, question, size):
    screen_codes = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"]
    screen_code = screen_codes[screen_id]

    if isinstance(question, str):
        question_dict = json.loads(question)  # Parse JSON string to dictionary
    else:
        question_dict = question.model_dump() 

    question_type = question_dict["type"]

    if question_type == "mcq":
        children_of_screen = mcqbuilder(screen_code, question, size)

    elif question_type == "scq":
        children_of_screen = scqbuilder(screen_code, question, size)

    else:
        children_of_screen = textbuilder(screen_code, question, size)
        
    screen = {
        "id" : f"screen_{screen_code}",
        "title" : f"Question {screen_id + 1}"
    }

    data = {}

    layout = {
        "type": "SingleColumnLayout",
        "children" : [
            {   
                "type": "Form",
                "name": "flow_path",
                "children": children_of_screen
            }
        ]   
    }

    if screen_id != 0:
        for i in range(screen_id):
            data.update(ELEMENT_DATA_DB[screen_codes[i]])

    screen.update({"data": data})

    if screen_id == size:   
        screen.update({"terminal": True})

    screen.update({"layout": layout})
    return screen



def jsonbuilder(prescreening_questions):
    size = len(prescreening_questions) - 1
    flow_json = {
        "version": "5.0",
        "screens": [screenbuilder(screen_id, prescreening_questions[screen_id], size) for screen_id in range(size+1)]
    }
    return flow_json
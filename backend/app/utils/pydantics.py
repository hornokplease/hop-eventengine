from pydantic import BaseModel

# used in app.api.root
class EventDetails(BaseModel):
    event_name : str 
    start_date : str
    end_date : str
    individual_cost: int
    max_cost: int
    max_attendees: int

class FrontendInput(BaseModel):
    events : list[EventDetails]

# used in app.utils.flowjson 
class AdditionalInfoEvent(BaseModel):
    event_name: str
    max_attendees: int

class AdditionalInfoPydantic(BaseModel):
    events: list[AdditionalInfoEvent]
from pydantic import BaseModel

class EventDetails(BaseModel):
    event_name : str 
    start_date : str
    end_date : str
    individual_cost: int
    max_cost: int
    max_attendees: int

class FrontendInput(BaseModel):
    events : list[EventDetails]
from pydantic import BaseModel
from datetime import date



class MembersInput(BaseModel):
    user_id     : int
    project_id  : int
    

class MembersResponse(BaseModel):
    id            : int
    user_id       : int
    user_photo    : str
    project_id    : int

    
    class Config:
        orm_mode = True
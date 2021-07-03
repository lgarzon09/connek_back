from pydantic import BaseModel
from datetime import date

class UsersInput(BaseModel):
    name         : str
    password      : str
    email         : str
    register_date : date
    photo_url     : str



class UsersResponse(BaseModel):
    id            : int
    name         : str
    password      : str
    email         : str
    register_date : date
    photo_url     : str
    
    class Config:
        orm_mode = True
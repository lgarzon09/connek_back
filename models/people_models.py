from pydantic import BaseModel
from datetime import date

class PeopleInput(BaseModel):
    user_id       : int
    phone         : str 
    birthday      : date          
    country       : str 
    city          : str 
    sector        : str 
    about         : str

class PeopleResponse(BaseModel):
    id             : int   
    user_id        : int
    user_name      : str 
    user_email     : str 
    user_photo     : str 
    phone          : str 
    birthday       : date          
    country        : str 
    city           : str 
    sector         : str 
    about          : str
    
    class Config:
        orm_mode = True
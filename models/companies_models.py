from pydantic import BaseModel
from datetime import date

class CompaniesInput(BaseModel):
    user_id       : int
    url           : str 
    birthday      : date          
    country       : str 
    city          : str 
    sector        : str 
    company_type  : str
    description   : str
    workers       : str

class CompaniesResponse(BaseModel):
    id             : int   
    user_id        : int
    user_name      : str 
    user_email     : str 
    user_photo     : str 
    url           : str 
    birthday      : date          
    country       : str 
    city          : str 
    sector        : str 
    company_type  : str
    description   : str
    workers       : str
    
    class Config:
        orm_mode = True
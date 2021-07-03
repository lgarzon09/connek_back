from pydantic import BaseModel
from datetime import datetime


class ProjectsInput(BaseModel):
    title          : str
    message        : str
    people_id      : int
    publish_date   : datetime
    close_date     : datetime
    photo_url      : str
    

class ProjectsUpdate(BaseModel):
    title          : str
    message        : str
    close_date     : datetime
    photo_url      : str
    

class ProjectsResponse(BaseModel):
    id               : int
    title            : str
    message          : str 
    people_id        : str
    publish_date     : datetime
    close_date       : datetime
    photo_url        : str
    
    class Config:
        orm_mode = True
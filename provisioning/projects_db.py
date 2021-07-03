from sqlalchemy                 import Column, DateTime, ForeignKey, Integer, String
from provisioning.connection_db import Base, engine
from datetime                   import datetime


class Projects(Base):
    __tablename__ = "projects"
    
    id             = Column(Integer,  primary_key=True, autoincrement=True, index=True)
    title          = Column(String,   nullable=False,   unique=True,        index=True)
    message        = Column(String,   nullable=False)
    people_id      = Column(Integer,   ForeignKey("people.id"))
    publish_date   = Column(DateTime, default=datetime.utcnow)
    close_date     = Column(DateTime, nullable=True)
    photo_url      = Column(String,   nullable=False)  


Base.metadata.create_all(bind=engine)
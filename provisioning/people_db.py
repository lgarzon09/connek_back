from sqlalchemy                 import Column, ForeignKey, Integer, String, Date
from provisioning.connection_db import Base, engine


class People(Base):
    __tablename__ = "people"
    
    id             = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id        = Column(Integer,  ForeignKey("users.id"))
    birthday       = Column(Date,     nullable=False)
    phone          = Column(String,   nullable=False)
    country        = Column(String,   nullable=False)
    city           = Column(String,   nullable=False)
    sector         = Column(String,   nullable=False)
    about          = Column(String,   nullable=False)
    

Base.metadata.create_all(bind=engine)
from sqlalchemy                 import Column, Integer, DateTime, String
from provisioning.connection_db import Base, engine
from datetime                   import datetime

class Users(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key= True, autoincrement=True, index=True)
    name          = Column(String, nullable=False)
    email         = Column(String, nullable=False)
    password      = Column(String, nullable=False)
    register_date = Column(DateTime, default=datetime.utcnow)
    photo_url     = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)
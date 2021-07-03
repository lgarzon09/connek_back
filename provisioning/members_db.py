from sqlalchemy                 import  Column, ForeignKey, Integer
from provisioning.connection_db import Base, engine


class Members(Base):
    __tablename__ = "members"
    
    id             = Column(Integer,  primary_key=True, autoincrement=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    

Base.metadata.create_all(bind=engine)
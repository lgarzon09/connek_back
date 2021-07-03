from sqlalchemy                 import Column, ForeignKey, Integer, String, Date
from provisioning.connection_db import Base, engine


class Companies(Base):
    __tablename__ = "companies"
    
    id             = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id        = Column(Integer,  ForeignKey("users.id"))
    birthday       = Column(Date,     nullable=False)
    url            = Column(String,   nullable=False)
    country        = Column(String,   nullable=False)
    city           = Column(String,   nullable=False)
    sector         = Column(String,   nullable=False)
    company_type   = Column(String,   nullable=False)
    description    = Column(String,   nullable=False)
    workers        = Column(String,   nullable=False)
    

Base.metadata.create_all(bind=engine)
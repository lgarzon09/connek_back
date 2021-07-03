import json
import pkgutil 
from   sqlalchemy                 import create_engine
from   sqlalchemy.ext.declarative import declarative_base
from   sqlalchemy.orm             import sessionmaker

pkg        = pkgutil.get_data(__name__, 'config.json').decode()
connection = json.loads(pkg)

db_user   = connection.get("db_user", {})
db_psswrd = connection.get("db_psswrd", {})
db_host   = connection.get("db_host", {})
db_port   = connection.get("db_port", {})
db_name   = connection.get("db_name", {})
db_schema = connection.get("db_schema", {})

SQLALCHEMY_DATABASE_URL = "postgresql://" + db_user + ":" + db_psswrd + "@" + db_host + ":" + db_port + "/" + db_name + ""
engine                  = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()
Base.metadata.schema = db_schema
                            
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from root import settings



database_uri = settings.DATABASE_URI

engine = create_engine(database_uri, connect_args={'check_same_thread': False})

session_local = sessionmaker(autocommit=False, autoflush=True, bind=engine)

db_base = declarative_base()

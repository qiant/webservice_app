from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# use sqlite 
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# use postgre docker container
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"


engine = create_engine(
    # using sqlite
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}

    # using postgresql, remove the connect_args
    #SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


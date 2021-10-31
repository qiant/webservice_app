from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=False, index=True)
    firstname = Column(String)
    lastname = Column(String)
    title = Column(String)
    description = Column(String)
    company = Column(String)


class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    email = Column(String)
    full_name = Column(String)
    disabled = Column(Boolean)
    hashed_password = Column(String)  
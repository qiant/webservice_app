from typing import List, Optional

from pydantic import BaseModel, Field

class ResumeBase(BaseModel):
    name: str = Field(None)  
    title: str = Field(None)
    description: str = Field(None)
    company: str = Field(None)

class ResumeCreate(ResumeBase):
    id: int = Field(None)
    firstname: str = Field(None)
    lastname: str = Field(None)
  

class Resume(ResumeBase):
    id: int  = Field(None)
  
    class Config:
        orm_mode = True

class ResumeID(BaseModel):
    id: int


class User(BaseModel):
    username: str
    email: str = Field(None)
    full_name: str = Field(None)
    disabled: bool = Field(None)


class UserInDB(User):
    hashed_password: str
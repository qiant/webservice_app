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
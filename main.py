from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

import redis

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
redisClient = redis.StrictRedis(host="localhost", port=6379, db=0)  #default localhost:6379, need to add password

#Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


@app.post("/api/uploadResumeDetails", response_model = schemas.ResumeID)
def upload_resume_details(resume: schemas.ResumeCreate, db: Session = Depends(get_db)): 
    """Takes in the body of the POST request, a json format of name, current job title, 
    current job description, current job company. Candidate name is in 
    <first name> space <last name> format. e.g. John<space>Doe
    The API Returns the generated resume ID in the response."""
    
    if resume.id != 0:
        db_resume = crud.get_resume_by_id(db, id = resume.id)
        if db_resume is not None and db_resume.id is not None:
          raise HTTPException(status_code=400, detail="Resume id exist, upload failed.")
    else: 
        resume.id = 0
        
    if ' ' not in resume.name:
        raise HTTPException(status_code=400, detail="Name is not <first>space<last> format.")
    
    splitname = resume.name.split(' ')
    if len(splitname) > 2:
        raise HTTPException(status_code=400, detail="Name is not <first>space<last> format.")

    resume.firstname, resume.lastname = splitname[0], splitname[1]
    if (not resume.firstname.isalnum()) or (not resume.lastname.isalnum()):
        raise HTTPException(status_code=400, detail="First name and last name must be alpha numeric chars only.")

    db_resume = crud.upload_resume(db, resume)
    
    return schemas.ResumeID(id = db_resume.id) 


@app.get("/api/getResumeById/{resume_id}", response_model = schemas.Resume)
def get_resume_by_id(resume_id: int, db: Session = Depends(get_db)):
    """Return the candidate resume details in same json format as uploaded when a 
    request is made to get a resume ID, it is returned."""
   
    db_resume = models.Resume() 
    id_str = str(resume_id) 
    if redisClient.exists(id_str):
        db_resume.id = resume_id
        db_resume.name = str(redisClient.hget(id_str, "name").decode("utf-8"))
        db_resume.title = str(redisClient.hget(id_str, "title").decode("utf-8"))
        db_resume.description = str(redisClient.hget(id_str, "description").decode("utf-8"))
        db_resume.company = str(redisClient.hget(id_str, "company").decode("utf-8"))
    else:
        db_resume = crud.get_resume_by_id(db, id = resume_id)
        if db_resume.id is None:
            return HTTPException(status_code=404, detail="Resume Id not found")
        
        redisClient.hset(id_str, "id", db_resume.id)
        redisClient.hset(id_str, "name", db_resume.name)
        redisClient.hset(id_str, "title", db_resume.title)
        redisClient.hset(id_str, "description", db_resume.description) 
        redisClient.hset(id_str, "company", db_resume.company)   
        
    return db_resume


@app.get("/api/getResumeByName/{name}", response_model = List[schemas.Resume])
def get_resume_by_name(name: str, db: Session = Depends(get_db)):
    """Returns resumes whose names match the given name. 
    Use URLEncoding (+ sign) in name input to denote space. e.g. john+doe for John Doe.
    
    In case both first name and last name do not BOTH match a candidate, 
    it should return resumes with matches for both first name and last name independently. 
    i.e. return all matches for John (in first name), and all matches for Doe (in last name)"""
    
    q_name = name
    if '+' not in name: 
       raise HTTPException(status_code=400, detail="Query resume name must be <first_name>+<last_name>")

    splitname = name.split("+")
    if len(splitname) > 2:
        raise HTTPException(status_code=400, detail="Query name must be <first_name>+<last_name> format.")

    first_name,last_name = splitname[0], splitname[1]
    if (not first_name.isalnum()) or (not last_name.isalnum()):
        raise HTTPException(status_code=400, detail="First name and last name must be alpha numeric chars only.")
    
    q_name = (first_name + " " + last_name).strip()
    
    db_resume = crud.get_resume_by_name(db, name = q_name)
    
    res = list()
    if db_resume.name is None:
        # query by first and last name, and group together
        res.extend(crud.get_resumes_by_firstname(db, firstname = first_name))
        res.extend(crud.get_resumes_by_lastname(db, lastname = last_name))        
    else: 
        res.append(db_resume)

    return res

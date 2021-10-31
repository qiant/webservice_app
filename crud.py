from sqlalchemy.orm import Session
from sqlalchemy import func

import models, schemas


def get_resume_by_id(db: Session, id: int):
    """Query table resumes with resume id."""

    res = db.query(models.Resume).filter(models.Resume.id == id).first()
    if res is None:
        return models.Resume()
    else: 
        return res

def get_resume_by_name(db: Session, name: str):
    """Query table resumes with full name <first_name>space<last_name>"""

    res = db.query(models.Resume).filter(models.Resume.name == name).first()
    if res is None:
        return models.Resume()
    else:
        return res # db.query(models.Resume).filter(models.Resume.name == name).first()

def get_resumes_by_firstname(db: Session, firstname: str, skip: int = 0, limit: int = 100):
    """Query table resumes with first_name"""
    
    #return db.query(models.Resume).filter(models.Resume.firstname == firstname).all()
    return db.query(models.Resume).filter(models.Resume.firstname == firstname).offset(skip).limit(limit).all()
    #return db.query(models.Resume).filter(models.Resume.firstname == firstname).first()

def get_resumes_by_lastname(db: Session, lastname: str, skip: int = 0, limit: int = 100):
    """Query table resumes with last_name"""
    
    return db.query(models.Resume).filter(models.Resume.lastname == lastname).offset(skip).limit(limit).all()
    #return db.query(models.Resume).filter(models.Resume.lastname == lastname).first()

def upload_resume(db: Session, resume: schemas.ResumeCreate):
    """Insert resume into table resumes. If resume_id is not given, find the next resume_id from table."""

    if resume.id == 0:
        new_id = db.query(func.max(models.Resume.id))
        resume.id = new_id
    db_resume =  models.Resume(id = resume.id, name = resume.name, firstname = resume.firstname, lastname = resume.lastname, title = resume.title, description = resume.description,company = resume.company)
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)

    return db_resume

def add_user(db: Session, user: schemas.UserInDB):
    db_user = models.User(username = user.username, hashed_password = user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user.username
    

def get_user(db: Session, name: str):
    """Query users table"""

    res = db.query(models.User).filter(models.User.username == name).first()
    return res
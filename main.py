from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from fastapi.responses import FileResponse
from pydantic import BaseModel

import crud, models, schemas
from database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def hello():
    return 'hello'

@app.get('/test')
def html_test():
    return FileResponse('index.html')

class Model(BaseModel):
    name: str
    phone: int

@app.post("/send")
def post_test(data: Model):
    print(data)
    return 'post success'


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)



@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
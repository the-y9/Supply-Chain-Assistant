from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt

from server.models import Base, engine, SessionLocal, User
from server.utils import hash_password, verify_password
from pydantic import BaseModel, EmailStr

router = APIRouter()

# Create tables if not already created
Base.metadata.create_all(bind=engine)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    active: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str

# JWT Config
JWT_SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter((User.email == user.email) | (User.username == user.username)).first():
        raise HTTPException(status_code=400, detail="Email or username already exists")

    hashed_pw = hash_password(user.password)
    new_user = User(email=user.email, username=user.username, password=hashed_pw, active=user.active)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user.active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

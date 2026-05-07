from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from app.models import User
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from app.schemas import UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Signup
@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # check email exists
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
         password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

# Login
# @router.post("/login")
# def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(
#         models.User.email == user.email
#     ).first()

#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if not verify_password(user.password, db_user.password):
#         raise HTTPException(status_code=401, detail="Invalid password")

#     token = create_access_token({"user_id": db_user.id})

#     return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    # 🔥 create token
    access_token = create_access_token(data={"user_id": db_user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
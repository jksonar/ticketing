from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas, security
from backend.database import get_db

router = APIRouter()

@router.get("/profile", response_model=schemas.User)
async def get_user_profile(db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    return current_user

@router.put("/profile", response_model=schemas.User)
async def update_user_profile(user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

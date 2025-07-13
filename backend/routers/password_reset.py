from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, security
from ..database import get_db

router = APIRouter()

@router.post("/request-password-reset", status_code=200)
async def request_password_reset(user_email: schemas.UserEmail, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_email.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # In a real application, you would send an email with a password reset link
    # For this example, we'll just return a dummy token
    token = security.create_access_token(data={"sub": user.email})
    return {"reset_token": token}

@router.post("/reset-password", status_code=200)
async def reset_password(password_reset: schemas.PasswordReset, db: Session = Depends(get_db)):
    user_email = security.verify_token(password_reset.token)
    if not user_email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = db.query(models.User).filter(models.User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = security.get_password_hash(password_reset.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

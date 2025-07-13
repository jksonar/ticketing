from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, security
from ..database import get_db
import uuid
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/invitations", response_model=schemas.Invitation)
async def create_invitation(invitation: schemas.InvitationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    # Check if the current user has permission to invite others to the project
    project = db.query(models.Project).filter(models.Project.id == invitation.project_id).first()
    if not project or current_user not in project.users:
        raise HTTPException(status_code=403, detail="Not authorized to invite users to this project")

    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=7)
    db_invitation = models.Invitation(**invitation.dict(), token=token, expires_at=expires_at)
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    # In a real application, you would send an email with the invitation link
    return db_invitation

@router.get("/invitations/{token}")
async def accept_invitation(token: str, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    invitation = db.query(models.Invitation).filter(models.Invitation.token == token).first()
    if not invitation or invitation.expires_at < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Invitation not found or has expired")

    project = db.query(models.Project).filter(models.Project.id == invitation.project_id).first()
    if current_user in project.users:
        raise HTTPException(status_code=400, detail="User is already a member of this project")

    project.users.append(current_user)
    db.delete(invitation)
    db.commit()
    return {"message": "Successfully joined the project"}

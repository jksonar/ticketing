from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, security
from ..database import get_db

router = APIRouter()

@router.get("/projects/{project_id}/settings", response_model=schemas.Project)
async def get_project_settings(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project or current_user not in project.users:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}/settings", response_model=schemas.Project)
async def update_project_settings(project_id: int, project_update: schemas.ProjectUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project or current_user not in project.users:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in project_update.dict(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

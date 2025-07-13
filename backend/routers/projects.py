from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, security
from ..database import get_db

router = APIRouter()

@router.post("/projects", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project: schemas.ProjectCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_project = models.Project(**project.dict())
    db_project.users.append(current_user)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/projects", response_model=List[schemas.Project])
def get_projects(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    return current_user.projects

@router.get("/projects/{project_id}", response_model=schemas.Project)
def get_project(
    project_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this project")
    return db_project

@router.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int, 
    project: schemas.ProjectUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this project")
    
    update_data = project.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if current_user not in db_project.users or current_user.role != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this project")
    
    db.delete(db_project)
    db.commit()
    return

@router.post("/projects/{project_id}/users", response_model=schemas.Project)
def add_user_to_project(
    project_id: int, 
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if current_user not in db_project.users or current_user.role not in ["Admin", "Team Lead"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add users to this project")
    
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db_project.users.append(db_user)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/projects/{project_id}/users/{user_id}", response_model=schemas.Project)
def remove_user_from_project(
    project_id: int, 
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if current_user not in db_project.users or current_user.role not in ["Admin", "Team Lead"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to remove users from this project")

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if db_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a member of this project")

    db_project.users.remove(db_user)
    db.commit()
    db.refresh(db_project)
    return db_project
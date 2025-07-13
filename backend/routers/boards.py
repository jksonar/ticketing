from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, security
from ..database import get_db

router = APIRouter()

@router.post("/boards", response_model=schemas.Board, status_code=status.HTTP_201_CREATED)
def create_board(
    board: schemas.BoardCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_project = db.query(models.Project).filter(models.Project.id == board.project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create boards in this project")

    db_board = models.Board(**board.dict())
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

@router.get("/projects/{project_id}/boards", response_model=List[schemas.Board])
def get_boards(
    project_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view boards in this project")

    return db_project.boards

@router.post("/columns", response_model=schemas.Column, status_code=status.HTTP_201_CREATED)
def create_column(
    column: schemas.ColumnCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_board = db.query(models.Board).filter(models.Board.id == column.board_id).first()
    if not db_board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    
    db_project = db_board.project
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create columns in this project")

    db_column = models.Column(**column.dict())
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column

@router.put("/columns/{column_id}", response_model=schemas.Column)
def update_column(
    column_id: int, 
    column: schemas.ColumnUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_column = db.query(models.Column).filter(models.Column.id == column_id).first()
    if not db_column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")

    db_project = db_column.board.project
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update columns in this project")

    update_data = column.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_column, key, value)
    
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column

@router.delete("/columns/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_column(
    column_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_column = db.query(models.Column).filter(models.Column.id == column_id).first()
    if not db_column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")

    db_project = db_column.board.project
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete columns in this project")

    db.delete(db_column)
    db.commit()
    return
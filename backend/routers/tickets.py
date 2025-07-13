from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, security
from ..database import get_db

router = APIRouter()

@router.post("/tickets", response_model=schemas.Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket: schemas.TicketCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    # Check if the column exists and if the user is a member of the project
    db_column = db.query(models.Column).filter(models.Column.id == ticket.column_id).first()
    if not db_column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")
    
    db_project = db_column.board.project
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create tickets in this project")

    db_ticket = models.Ticket(**ticket.dict(), owner_id=current_user.id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.get("/tickets", response_model=List[schemas.Ticket])
def get_tickets(
    project_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user),
    search: str = None,
    status: str = None,
    priority: str = None,
    owner_id: int = None
):
    # Check if the user is a member of the project
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view tickets in this project")

    query = db.query(models.Ticket).join(models.Column).join(models.Board).filter(models.Board.project_id == project_id)

    if search:
        query = query.filter(models.Ticket.title.contains(search) | models.Ticket.description.contains(search))
    if status:
        query = query.filter(models.Ticket.status == status)
    if priority:
        query = query.filter(models.Ticket.priority == priority)
    if owner_id:
        query = query.filter(models.Ticket.owner_id == owner_id)

    return query.all()

@router.get("/tickets/{ticket_id}", response_model=schemas.Ticket)
def get_ticket(
    ticket_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    
    db_project = db_ticket.column.board.project
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this ticket")

    return db_ticket

@router.put("/tickets/{ticket_id}", response_model=schemas.Ticket)
def update_ticket(
    ticket_id: int, 
    ticket: schemas.TicketUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    db_project = db_ticket.column.board.project
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this ticket")

    update_data = ticket.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ticket, key, value)
    
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    db_project = db_ticket.column.board.project
    if current_user not in db_project.users or current_user.role not in ["Admin", "Team Lead"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this ticket")

    db.delete(db_ticket)
    db.commit()
    return

@router.get("/tickets/{ticket_id}/history", response_model=List[schemas.TicketHistory])
def get_ticket_history(
    ticket_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    db_project = db_ticket.column.board.project
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view ticket history")

    return db_ticket.history

@router.post("/tickets/{ticket_id}/comments", response_model=schemas.Comment, status_code=status.HTTP_201_CREATED)
def create_comment(
    ticket_id: int, 
    comment: schemas.CommentCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    db_project = db_ticket.column.board.project
    if current_user not in db_project.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to comment on this ticket")

    db_comment = models.Comment(**comment.dict(), author_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
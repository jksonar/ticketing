from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "Developer"

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class User(UserBase):
    id: int
    role: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    description: Optional[str] = None

class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    users: List[User] = []

    class Config:
        orm_mode = True

# Board Schemas
class BoardBase(BaseModel):
    name: str

class BoardCreate(BoardBase):
    project_id: int

class BoardUpdate(BoardBase):
    name: Optional[str] = None

class Board(BoardBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Column Schemas
class ColumnBase(BaseModel):
    name: str

class ColumnCreate(ColumnBase):
    board_id: int

class ColumnUpdate(ColumnBase):
    name: Optional[str] = None

class Column(ColumnBase):
    id: int
    board_id: int

    class Config:
        orm_mode = True

# Ticket Schemas
class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None

class TicketCreate(TicketBase):
    column_id: int

class TicketUpdate(TicketBase):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    owner_id: Optional[int] = None
    column_id: Optional[int] = None

class Ticket(TicketBase):
    id: int
    owner_id: Optional[int] = None
    column_id: int
    status: str
    priority: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Comment Schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    ticket_id: int

class CommentUpdate(CommentBase):
    content: Optional[str] = None

class Comment(CommentBase):
    id: int
    ticket_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Ticket History Schemas
class TicketHistoryBase(BaseModel):
    field_changed: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None

class TicketHistoryCreate(TicketHistoryBase):
    ticket_id: int
    changed_by_id: int

class TicketHistory(TicketHistoryBase):
    id: int
    ticket_id: int
    changed_by_id: int
    changed_at: datetime

    class Config:
        orm_mode = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Password Reset Schemas
class UserEmail(BaseModel):
    email: str

class PasswordReset(BaseModel):
    token: str
    new_password: str

# Invitation Schemas
class InvitationBase(BaseModel):
    email: str
    project_id: int

class InvitationCreate(InvitationBase):
    pass

class Invitation(InvitationBase):
    id: int
    token: str
    expires_at: datetime

    class Config:
        orm_mode = True
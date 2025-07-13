from fastapi import FastAPI, Request, status, WebSocket, WebSocketDisconnect
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .database import engine, Base
from .routers import authentication, projects, tickets, boards

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Jira Clone API",
    description="A FastAPI-powered backend for a Jira-like ticketing system.",
    version="0.1.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message text was: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Include API routers
app.include_router(authentication.router, prefix="/api", tags=["Authentication"])
app.include_router(projects.router, prefix="/api", tags=["Projects"])
app.include_router(tickets.router, prefix="/api", tags=["Tickets"])
app.include_router(boards.router, prefix="/api", tags=["Boards"])

@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

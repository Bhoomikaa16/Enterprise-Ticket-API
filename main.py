from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Initialize FastAPI App
app = FastAPI(
    title="Enterprise IT Ticket & Support API",
    description="RESTful API for tracking enterprise IT incidents and maintenance requests.",
    version="1.0.0"
)

# Data Schema for a Support Ticket
class Ticket(BaseModel):
    id: int
    title: str
    description: str
    department: str  # e.g., "Chemical Operations", "IT Infrastructure", "Logistics"
    priority: str    # "High", "Medium", "Low"
    status: str      # "Open", "In Progress", "Resolved"

# In-memory database array
tickets_db: List[Ticket] = [
    Ticket(
        id=101,
        title="Database Latency Spike",
        description="High query times on main production server.",
        department="IT Infrastructure",
        priority="High",
        status="Open"
    )
]

# Route 1: Health Check / Root Endpoint
@app.get("/")
def root():
    return {"status": "Active", "message": "Enterprise Ticket API is running."}

# Route 2: Get all tickets
@app.get("/tickets", response_model=List[Ticket])
def get_all_tickets():
    return tickets_db

# Route 3: Create a new ticket
@app.post("/tickets", response_model=Ticket)
def create_ticket(ticket: Ticket):
    # Prevent duplicate IDs
    for existing_ticket in tickets_db:
        if existing_ticket.id == ticket.id:
            raise HTTPException(status_code=400, detail="Ticket ID already exists.")
    
    tickets_db.append(ticket)
    return ticket

# Route 4: Fetch a specific ticket by ID
@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket_by_id(ticket_id: int):
    for ticket in tickets_db:
        if ticket.id == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found.")
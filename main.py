from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 1. Database Setup (SQLite)
DATABASE_URL = "sqlite:///./tickets.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Database Model
class TicketDB(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    department = Column(String)
    priority = Column(String)
    status = Column(String, default="Open")

Base.metadata.create_all(bind=engine)

# 3. Pydantic Schemas
class TicketCreate(BaseModel):
    title: str
    description: str
    department: str
    priority: str

class TicketResponse(TicketCreate):
    id: int
    status: str

    class Config:
        from_attributes = True

# 4. Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 5. FastAPI App & Routes
app = FastAPI(title="Enterprise Incident Management API", version="2.0.0")

@app.post("/tickets/", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = TicketDB(**ticket.model_dump())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@app.get("/tickets/", response_model=List[TicketResponse])
def get_tickets(priority: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(TicketDB)
    if priority:
        query = query.filter(TicketDB.priority == priority)
    return query.all()

@app.put("/tickets/{ticket_id}/status", response_model=TicketResponse)
def update_status(ticket_id: int, status: str, db: Session = Depends(get_db)):
    ticket = db.query(TicketDB).filter(TicketDB.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.status = status
    db.commit()
    db.refresh(ticket)
    return ticket

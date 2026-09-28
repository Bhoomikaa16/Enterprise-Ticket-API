# Enterprise Incident & Support Ticket REST API

An asynchronous RESTful service built using Python, FastAPI, and SQLAlchemy ORM to manage enterprise IT incidents, equipment tracking, and workflow status updates.

## Key Features
- **Persistent Storage**: Integrated SQLite database using SQLAlchemy ORM for reliable data persistence across sessions.
- **Dynamic Query Filtering**: Filter support tickets by priority levels (`High`, `Medium`, `Low`).
- **Status Lifecycle Management**: Dedicated endpoints to update ticket status (`Open` -> `In Progress` -> `Resolved`).
- **Automated Validation**: Pydantic schemas enforcing strict request payload typing and error handling.

## API Endpoint Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/tickets/` | Create a new support ticket |
| `GET` | `/tickets/` | Fetch all tickets (supports `?priority=High` filter) |
| `PUT` | `/tickets/{id}/status` | Update resolution status of a ticket |

## Architecture & Tech Stack
- **Framework**: FastAPI (Python 3.10+)
- **Database**: SQLite with SQLAlchemy ORM
- **Validation**: Pydantic v2
- **Server**: Uvicorn ASGI Server

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Bhoomikaa16/Enterprise-Ticket-API.git](https://github.com/Bhoomikaa16/Enterprise-Ticket-API.git)

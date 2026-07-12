# AI-First CRM HCP Module – Log Interaction Screen

## Overview

This project is an AI-first Customer Relationship Management (CRM) application designed for Life Sciences field representatives. It focuses on the Healthcare Professional (HCP) module, allowing users to log interactions with doctors through either a structured form or an AI-powered conversational interface.

The application leverages LangGraph and Groq LLMs to automate interaction summarization, entity extraction, follow-up recommendations, and CRM record management.

---

## Features

### Log Interaction

- Log HCP interactions using a structured form.
- AI-powered conversational logging.
- Automatic interaction summarization.
- Entity extraction (Doctor, Product, Date, Interaction Type).
- Sentiment analysis.
- Save interaction to database.

### Edit Interaction

- Modify previously logged interactions.
- Update interaction details.
- Save edited records to the database.

### Search HCP

- Search Healthcare Professionals.
- View doctor profile.
- Access previous interaction history.

### Interaction History

- Display all previous interactions with an HCP.
- Sort and filter interaction records.

### Follow-up Management

- AI-generated next action recommendations.
- Schedule reminders and follow-up tasks.

---

# Tech Stack

## Frontend

- React
- Redux Toolkit
- React Router
- Axios
- Google Inter Font

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL / MySQL

## AI Stack

- LangGraph
- LangChain
- Groq API
- Gemma2-9B-IT
- Llama-3.3-70B-Versatile (optional)

---

# AI Agent

The application uses a LangGraph-based AI agent responsible for managing HCP interactions.

The AI agent performs:

- Natural language understanding
- Tool selection
- Interaction summarization
- Entity extraction
- CRM record updates
- Follow-up recommendations

---

# LangGraph Tools

## 1. Log Interaction

Captures user conversations and automatically:

- Generates interaction summary
- Extracts HCP name
- Extracts discussed products
- Detects sentiment
- Saves interaction

---

## 2. Edit Interaction

Allows users to:

- Update interaction notes
- Modify interaction details
- Save changes

---

## 3. Search HCP

Retrieves:

- HCP profile
- Specialty
- Previous interactions

---

## 4. Get Interaction History

Displays:

- Complete visit history
- Previous notes
- Interaction timeline

---

## 5. Create Follow-up

Creates:

- Follow-up reminders
- Suggested next actions
- CRM tasks

---

# Project Structure

```
ai-crm-hcp/

├── backend/
│   ├── app/
│   │   ├── ai_agent/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── database.py
│   ├── requirements.txt
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── redux/
│   │   ├── services/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── .env
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/ai-crm-hcp.git

cd ai-crm-hcp
```

---

# Backend Setup

```bash
cd backend

python -m venv venv
```

Activate virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure the `.env` file:

```
DATABASE_URL=postgresql://username:password@localhost:5432/crm
GROQ_API_KEY=your_groq_api_key
```

Run backend

```bash
uvicorn app.main:app --reload
```

Backend runs at

```
http://localhost:8000
```

---

# Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at

```
http://localhost:5173
```

---

# AI Workflow

```
User
   │
   ▼
React UI
   │
   ▼
FastAPI
   │
   ▼
LangGraph Agent
   │
   ├── Log Interaction
   ├── Edit Interaction
   ├── Search HCP
   ├── Get Interaction History
   └── Create Follow-up
   │
   ▼
Groq LLM
   │
   ▼
Database
```

---

# Database

Main tables:

- Users
- Healthcare Professionals (HCP)
- Interactions
- Follow-ups

---

# Future Improvements

- Voice-based interaction logging
- OCR support for doctor's prescriptions
- Offline synchronization
- Analytics dashboard
- Calendar integration
- Multi-language support

---

# Assignment Requirements Covered

- React Frontend
- Redux State Management
- FastAPI Backend
- LangGraph AI Agent
- Groq LLM Integration
- Structured Form
- Conversational Chat Interface
- Five AI Tools
- PostgreSQL/MySQL Support
- Interaction Logging
- Interaction Editing
- AI Summarization
- Entity Extraction

---

# Author

Assignment Submission for **AI-First CRM HCP Module – Log Interaction Screen**

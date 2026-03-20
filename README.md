# DesignMate AI

## Overview
- AI-powered interior design MVP
- Input: room type, dimensions, budget, style, colors, notes, optional room photo
- Output: 3 initial design concepts with item list, prices, and retailer info
- Current data source: local mock catalog
- Current UI: Streamlit
- Current workflow engine: LangGraph

## Current MVP Scope
- Collects room preferences from a simple UI
- Runs a 3-step graph:
  - analyze room
  - retrieve candidates
  - generate options
- Loads furniture from `data/catalog.json`
- Returns budget-aware starter concepts
- Includes a tiny FastAPI health endpoint

## Not Built Yet
- Real room vision analysis
- Live Amazon / IKEA / retailer integrations
- Real optimization with OR-Tools
- Photorealistic rendering / AR view
- Persistent database / auth / multi-user support

## Tech Stack
- Python
- Streamlit
- LangGraph
- Pydantic
- OR-Tools
- FastAPI
- Uvicorn
- Pillow
- OpenAI SDK
- python-dotenv

## Project Structure
- `app.py` — Streamlit app entry point
- `agents/state.py` — shared request/state/data models
- `agents/nodes.py` — graph nodes
- `agents/graph.py` — LangGraph flow definition
- `services/catalog.py` — catalog loading + shortlisting
- `services/optimizer.py` — initial option-building logic
- `services/api.py` — FastAPI health endpoint
- `data/catalog.json` — mock furniture catalog
- `.env.example` — env variable template
- `requirements.txt` — Python dependencies

## Prerequisites
- Python 3.10+
- Git
- VS Code recommended

## Clone and Run From GitHub
- Clone repo
  - `git clone <your-repo-url>`
- Move into project folder
  - `cd designmate`
- Create virtual environment
  - Windows PowerShell: `python -m venv .venv`
  - macOS/Linux: `python3 -m venv .venv`
- Activate virtual environment
  - Windows PowerShell: `.venv\Scripts\Activate.ps1`
  - macOS/Linux: `source .venv/bin/activate`
- Install dependencies
  - `pip install -r requirements.txt`
- Run Streamlit app
  - `streamlit run app.py`
- Optional: run FastAPI health server
  - `uvicorn services.api:app --reload`

## App URLs
- Streamlit app
  - usually `http://localhost:8501`
- FastAPI health
  - usually `http://127.0.0.1:8000/health`

## Environment Variables
- Current MVP can run without an API key
- For future OpenAI features:
  - copy `.env.example` to `.env`
  - add your key in `.env`
- Example:
  - `OPENAI_API_KEY=your_key_here`

## Install Dependencies Manually
- Main packages in `requirements.txt`
  - `streamlit`
  - `langgraph`
  - `pydantic`
  - `python-dotenv`
  - `ortools`
  - `fastapi`
  - `uvicorn[standard]`
  - `openai`
  - `pillow`

## How the Current Flow Works
- User enters room inputs in sidebar
- App creates `RoomInput`
- Graph runs:
  - `analyze_room()`
  - `retrieve_candidates()`
  - `generate_options()`
- Results are rendered as concept cards
- Raw graph output is shown for debugging

## What Teammates Can Work On
- `services/optimizer.py`
  - replace heuristic logic with OR-Tools
- `services/catalog.py`
  - add live product adapters / normalization
- `agents/nodes.py`
  - add more graph nodes and better reasoning steps
- `agents/state.py`
  - expand shared schema safely
- `app.py`
  - improve UX, forms, previews, filters
- `data/catalog.json`
  - extend test catalog
- `services/api.py`
  - add endpoints for future frontend/backend split

## Recommended Contribution Rules
- Pull latest code before starting
  - `git pull origin main`
- Create a feature branch
  - `git checkout -b feature/<name>`
- Keep changes scoped to one module when possible
- Test app locally before pushing
- Commit with clear messages
- Open PR / merge after review

## Suggested Branch Examples
- `feature/optimizer-ortools`
- `feature/product-adapters`
- `feature/vision-input`
- `feature/ui-upgrades`
- `feature/rendering-pipeline`

## Local Test Checklist
- App starts without errors
- Sidebar accepts all inputs
- Generate button returns concepts
- Item prices load correctly
- No broken imports
- FastAPI `/health` returns `{"status": "ok"}`

## Common Commands
- Start app
  - `streamlit run app.py`
- Start API
  - `uvicorn services.api:app --reload`
- Freeze packages if needed
  - `pip freeze > requirements.txt`
- Deactivate venv
  - `deactivate`

## Common Issues
- `requirements.txt not found`
  - make sure terminal is inside project root
- venv activation blocked on Windows
  - `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
- import errors
  - confirm venv is active
  - reinstall: `pip install -r requirements.txt`
- port already in use
  - stop old Streamlit/Uvicorn process

## Git Ignore
- Do not commit:
  - `.venv/`
  - `__pycache__/`
  - `.env`
  - `.streamlit/secrets.toml`
  - local temp/cache files

## Recommended `.gitignore`
```gitignore
.venv/
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
```

## Next Build Priorities
- Add OR-Tools optimization
- Add product-provider interface
- Add real retailer sources
- Save uploaded images properly
- Add vision analysis step
- Add rendering / in-room preview pipeline

## MVP Goal
- Simple app
- Clean graph workflow
- Easy for teammates to extend
- Safe base before adding real APIs and rendering

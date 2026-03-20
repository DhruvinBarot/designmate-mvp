# DesignMate AI 

This scaffold turns the project proposal into a practical MVP for today's session.

## What this version does
- Collects room preferences from a simple Streamlit UI
- Runs a small LangGraph workflow
- Loads a mock furniture catalog from JSON
- Produces 3 initial design options
- Keeps the code split into agent, services, and data modules

## What is intentionally mocked for now
- Vision-based room analysis
- Live retailer APIs
- Real vector search
- Photorealistic rendering

## Suggested next checkpoints
1. Replace heuristic design generation with OR-Tools optimization
2. Add image analysis with an LLM vision model
3. Add live product adapters
4. Add render prompt generation or image compositing

## Setup
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
streamlit run app.py
```

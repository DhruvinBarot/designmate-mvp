from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="DesignMate API", version="0.1.0")


@app.get("/health")
def healthcheck():
    return {"status": "ok"}

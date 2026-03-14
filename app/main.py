from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .engine import NeuroEngine
import os

app = FastAPI(title="Neuro-Vault Knowledge API")

# Initialize engine (expects OPENAI_API_KEY in env)
engine = NeuroEngine(api_key=os.getenv("OPENAI_API_KEY", "default_key"))

class IngestRequest(BaseModel):
    content: str
    source: str

class QueryRequest(BaseModel):
    query: str

@app.post("/ingest")
async def ingest_knowledge(request: IngestRequest):
    engine.ingest(request.content, request.source)
    return {"message": "Knowledge successfully optimized and vaulted."}

@app.post("/query")
async def query_vault(request: QueryRequest):
    try:
        insight = engine.generate_insight(request.query)
        return {"insight": insight}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "active", "vault_size": len(engine.memory_vault)}
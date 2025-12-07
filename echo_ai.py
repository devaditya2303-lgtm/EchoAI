# echo_ai.py
import os
import re
import asyncio
from typing import Optional, List
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from duckduckgo_search import DDGS
# If using local LLM:
# from llama_cpp import Llama

# ----------------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------------
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "true").lower() in ("1","true","yes")
# Path to local llama / other model if using
LOCAL_LLM_MODEL_PATH = os.getenv("LOCAL_LLM_MODEL_PATH", "models/llama-7B/ggml-model.bin")

app = FastAPI(title="EchoAI Backend")

# ----------------------------------------------------------------------------
# Helper: decide mode math/knowledge vs chat
# ----------------------------------------------------------------------------
MATH_KW = [r"\bsolve\b", r"\bderivative\b", r"[0-9]+\s*[\+\-\*\/\^]", r"\blimit\b", r"\bvalue of\b"]
FACT_KW = [r"what is", r"who is", r"when", r"where", r"explain", r"history", r"define", r"why"]

def needs_knowledge(q: str) -> bool:
    q_l = q.lower()
    if re.search(r"[0-9]+\s*[\+\-\*\/\^]", q):
        return True
    for kw in MATH_KW + FACT_KW:
        if re.search(kw, q_l):
            return True
    return False

# ----------------------------------------------------------------------------
# Models
# ----------------------------------------------------------------------------
class QueryIn(BaseModel):
    query: str
    mode: Optional[str] = "auto"  # "auto", "search", "chat"
    max_results: Optional[int] = 5

class Source(BaseModel):
    title: str
    link: str
    snippet: str

class Answer(BaseModel):
    route: str  # "knowledge" or "chat"
    answer: str
    sources: Optional[List[Source]] = None

# ----------------------------------------------------------------------------
# Knowledge via DuckDuckGo search
# ----------------------------------------------------------------------------
async def search_ddg(query: str, max_results: int = 5) -> List[Source]:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.search(query, max_results=max_results):
            results.append(Source(
                title=r.get("title"),
                link=r.get("href"),
                snippet=r.get("body") or ""
            ))
    return results

# ----------------------------------------------------------------------------
# Chat via local LLM (example using llama_cpp) — placeholder
# ----------------------------------------------------------------------------
def local_llm_chat(prompt: str) -> str:
    """
    Replace this with actual llama_cpp or other open-source model inference code.
    For now, it returns prompt (dummy).
    """
    # Example (uncomment when llama_cpp installed):
    # llama = Llama(model_path=LOCAL_LLM_MODEL_PATH, n_ctx=512)
    # out = llama(prompt, max_tokens=256, temperature=0.7)
    # return out["choices"][0]["text"]
    return "🎵 EchoAI says: I’m still learning — but I hear you: " + prompt[:200]

# ----------------------------------------------------------------------------
# API endpoint
# ----------------------------------------------------------------------------
@app.post("/query", response_model=Answer)
async def handle_query(q: QueryIn):
    user_q = q.query.strip()
    if not user_q:
        raise HTTPException(status_code=400, detail="Empty query")
    # route decision
    if q.mode == "search":
        route = "knowledge"
    elif q.mode == "chat":
        route = "chat"
    else:
        route = "knowledge" if needs_knowledge(user_q) else "chat"

    if route == "knowledge":
        sources = await search_ddg(user_q, max_results=q.max_results or 5)
        # build answer: simple merge of top snippet + links
        ans = "Here’s what I found for you:\n\n"
        for i, s in enumerate(sources, start=1):
            ans += f"{i}. {s.title}\n   Snippet: {s.snippet}\n   Link: {s.link}\n\n"
        return Answer(route="knowledge", answer=ans, sources=sources)
    else:
        # chat route
        if USE_LOCAL_LLM:
            resp = local_llm_chat(user_q)
        else:
            resp = "Hello — EchoAI here! (Set up LLM to get real chat responses.)"
        return Answer(route="chat", answer=resp, sources=None)

# ----------------------------------------------------------------------------
# Run with: uvicorn echo_ai:app --reload
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("echo_ai:app", host="0.0.0.0", port=8000, reload=True)

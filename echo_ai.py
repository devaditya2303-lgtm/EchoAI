from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from duckduckgo_search import DDGS
from pydantic import BaseModel
import pathlib

# ---------------------------------------------------------
# TEMPLATE ENGINE SETUP
# ---------------------------------------------------------
BASE_DIR = pathlib.Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# ---------------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------------
app = FastAPI(title="EchoAI")

# ---------------------------------------------------------
# INPUT MODEL
# ---------------------------------------------------------
class Query(BaseModel):
    query: str
    mode: str  # "auto", "search", "chat"

# ---------------------------------------------------------
# SEARCH MODE (DuckDuckGo)
# ---------------------------------------------------------
def search_google_free(query: str):
    """Uses DuckDuckGo search (free, zero cost)."""
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        return results

# ---------------------------------------------------------
# CHAT MODE (Simple AI reply)
# ---------------------------------------------------------
def chat_response(user_msg: str):
    # You can upgrade this later with a local LLM
    return f"EchoAI 🤖: Haha nice! You said — '{user_msg}'. I'm still learning to chat like a human!"

# ---------------------------------------------------------
# AUTO ROUTING
# ---------------------------------------------------------
def auto_route(query: str):
    academic_keywords = [
        "calculate", "solve", "define", "explain", "what is",
        "derivative", "chemistry", "physics", "formula",
        "math", "who is", "where is", "history", "jee", "neet"
    ]

    for word in academic_keywords:
        if word in query.lower():
            return "search"

    return "chat"

# ---------------------------------------------------------
# API ENDPOINT FOR CHAT / SEARCH
# ---------------------------------------------------------
@app.post("/query")
async def answer(q: Query):
    query = q.query
    mode = q.mode

    # Auto mode routing
    if mode == "auto":
        mode = auto_route(query)

    # SEARCH MODE
    if mode == "search":
        results = search_google_free(query)
        return JSONResponse({
            "route": "search",
            "answer": "Here’s what I found online:",
            "sources": results
        })

    # CHAT MODE
    if mode == "chat":
        reply = chat_response(query)
        return JSONResponse({
            "route": "chat",
            "answer": reply
        })

    # DEFAULT CASE
    return JSONResponse({"answer": "Unknown mode!"})

# ---------------------------------------------------------
# HOMEPAGE ROUTE (SERVES index.html)
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

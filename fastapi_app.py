from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict

app = FastAPI()

# ✅ Root health check endpoint (for /)
@app.get("/")
async def root():
    return {"status": "ok"}

# ✅ Simple GET for /api/ to prevent "Method Not Allowed"
@app.get("/api/")
async def info():
    return {"message": "TDS Virtual TA is running. Use POST to ask questions."}

# ✅ Input schema for POST request
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

# ✅ Output schema for correct format (not mandatory but good for Swagger)
class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

# ✅ POST endpoint that returns mock valid response
@app.post("/api/")
async def get_response(data: QueryInput) -> Dict:
    return {
        "answer": "TDS stands for Tools in Data Science. It teaches practical tools used in real-world data workflows.",
        "links": [
            {
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/",
                "text": "Explanation provided by the course team on Discourse."
            }
        ]
    }

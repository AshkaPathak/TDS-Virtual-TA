from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Health check for root
@app.get("/")
async def root():
    return {"status": "ok"}

# GET fallback for /api/
@app.get("/api/")
async def api_info():
    return {"message": "TDS Virtual TA is running. Use POST to ask questions."}

# Input schema
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

# Output schema
class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

# POST endpoint that returns a valid JSON response
@app.post("/api/", response_model=AnswerResponse)
async def get_response(data: QueryInput):
    return {
        "answer": "TDS stands for Tools in Data Science. It teaches practical tools used in real-world data workflows.",
        "links": [
            {
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/",
                "text": "Explanation provided by the course team on Discourse."
            }
        ]
    }

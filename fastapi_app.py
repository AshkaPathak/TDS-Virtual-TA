from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Health check
@app.get("/")
async def health_check():
    return {"status": "ok"}

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

# ✅ POST route should now be root "/"
@app.post("/")
async def respond(data: QueryInput) -> AnswerResponse:
    return {
        "answer": "TDS stands for Tools in Data Science. It teaches practical tools used in real-world data workflows.",
        "links": [
            {
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/",
                "text": "Explanation provided by the course team on Discourse."
            }
        ]
    }

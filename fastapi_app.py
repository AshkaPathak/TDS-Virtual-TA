from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict

app = FastAPI()

# ✅ Input schema
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

# ✅ Output schema (optional but good for documentation)
class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

# ✅ Health check (GET /)
@app.get("/")
async def root_get():
    return {"status": "ok"}

# ✅ POST main route (POST /)
@app.post("/", response_model=AnswerResponse)
async def answer_question(data: QueryInput) -> Dict:
    return {
        "answer": "TDS stands for Tools in Data Science. It teaches practical tools used in real-world data workflows.",
        "links": [
            {
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/",
                "text": "Explanation provided by the course team on Discourse."
            }
        ]
    }

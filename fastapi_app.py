from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/api/")
async def get_api_info():
    return {"message": "Use POST to interact."}

class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

@app.post("/api/")
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

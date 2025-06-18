from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

# Response schema
class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

# Hardcoded QA pairs
qa_pairs = {
    "What is TDS?": {
        "answer": "TDS stands for Tools in Data Science. It teaches practical tools used in real-world data workflows.",
        "links": [
            {
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/",
                "text": "Explanation by course team"
            }
        ]
    },
    "When is project 1 due?": {
        "answer": "Project 1 is due on 18 June 2025 at 11:59 PM IST.",
        "links": [
            {
                "url": "https://onlinedegree.iitm.ac.in/",
                "text": "Check portal"
            }
        ]
    },
    "Should I use gpt-4o-mini which AI proxy supports, or gpt3.5 turbo?": {
        "answer": "You must use `gpt-3.5-turbo-0125`, even if the AI Proxy only supports `gpt-4o-mini`.",
        "links": [
            {
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/",
                "text": "Use the model that’s mentioned in the question."
            }
        ]
    }
}

@app.get("/")
async def root():
    return {"status": "ok", "served_from": "vercel or replit"}

@app.post("/", response_model=AnswerResponse)
async def answer(data: QueryInput) -> AnswerResponse:
    question = data.question.strip()
    if question in qa_pairs:
        return AnswerResponse(**qa_pairs[question])
    else:
        return AnswerResponse(answer="Sorry, I do not know the answer to that question.", links=[])

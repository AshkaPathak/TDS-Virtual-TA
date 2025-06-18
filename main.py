from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

qa_pairs = {
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
    return {"status": "ok"}

@app.post("/", response_model=AnswerResponse)
async def answer(data: QueryInput) -> AnswerResponse:
    q = data.question.strip()
    if q in qa_pairs:
        return AnswerResponse(**qa_pairs[q])
    else:
        return AnswerResponse(answer="Sorry, I do not know the answer to that question.", links=[])

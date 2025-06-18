from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import os
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub

app = FastAPI()

# Schema
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

# Load FAISS index
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

# Template to frame a good answer
template = """You are a helpful TA for the TDS course. Answer clearly and concisely.
Question: {question}
Relevant context: {context}
Answer:"""
prompt = PromptTemplate.from_template(template)

# Use mock LLM (replace with OpenAI or HuggingFaceHub for real answers)
class MockLLM:
    def invoke(self, prompt: str):
        return "🤖 This is a placeholder answer. Please run locally with OpenAI or HuggingFaceHub for real responses."

llm = MockLLM()

@app.get("/")
async def root():
    return {"status": "ok", "served_from": "vercel"}

@app.post("/", response_model=AnswerResponse)
async def answer(data: QueryInput) -> AnswerResponse:
    question = data.question.strip()
    docs = db.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt_with_context = prompt.format(question=question, context=context)
    response = llm.invoke(prompt_with_context)
    return AnswerResponse(answer=response, links=[])

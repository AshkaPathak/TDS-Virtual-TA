from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate

app = FastAPI()

# Root route to verify deployment success
@app.get("/")
async def root():
    return {"message": "✅ TDS Virtual TA is running. Visit /docs for Swagger UI."}

# Load FAISS index
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

# Fallback LLM when LLaMA/OpenAI isn't usable
class MockLLM:
    def invoke(self, prompt):
        return "This is a placeholder answer. Please run locally with LLaMA or OpenAI for real responses."

llm = MockLLM()

# Request schema
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

# /api/ endpoint
@app.post("/api/")
async def get_response(data: QueryInput):
    docs = db.similarity_search(data.question, k=3)

    if not docs:
        return {
            "answer": "❌ Sorry, I couldn't find a relevant answer. Try rephrasing.",
            "links": []
        }

    context = "\n\n".join([doc.page_content for doc in docs])
    links = [
        {"url": doc.metadata.get("source", ""), "text": doc.metadata.get("source", "")}
        for doc in docs
    ]

    prompt = PromptTemplate.from_template("""
You are a helpful Virtual TA for the TDS course.
Use the following context to answer the student's question.

Context:
{context}

Question:
{question}

Answer:
""")

    try:
        final_answer = llm.invoke(
            prompt.format(context=context, question=data.question)
        ).strip()
    except Exception as e:
        final_answer = f"⚠️ Error generating answer: {str(e)}"

    return {
        "answer": final_answer,
        "links": links
    }

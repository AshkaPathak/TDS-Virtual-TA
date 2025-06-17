from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os

from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate

app = FastAPI()

# Root route to verify deployment
@app.get("/")
async def root():
    return {"message": "✅ TDS Virtual TA is running. Visit /docs for Swagger UI."}

# Load embedding model
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load FAISS index (ensure 'faiss_index' exists in your project root)
db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

# Mock LLM for deployment fallback
class MockLLM:
    def invoke(self, prompt):
        return "🤖 This is a placeholder answer. Please run locally with LLaMA or OpenAI for real responses."

llm = MockLLM()

# Define request schema
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

# Define API route
@app.post("/api/")
async def get_response(data: QueryInput):
    docs = db.similarity_search(data.question)
    content = "\n\n".join([doc.page_content for doc in docs])
    
    # Template used for constructing prompt
    prompt = PromptTemplate.from_template(
        "You're a teaching assistant for the TDS course. Use the following context:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"
    )
    
    full_prompt = prompt.format(context=content, question=data.question)
    result = llm.invoke(full_prompt)

    return {"answer": result}

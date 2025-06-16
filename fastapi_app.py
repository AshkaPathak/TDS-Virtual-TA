from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import requests

app = FastAPI()

# Load FAISS index
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

# Input schema
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

@app.post("/api/")
async def get_response(data: QueryInput):
    docs = db.similarity_search(data.question, k=3)

    if not docs:
        return {
            "answer": "❌ Sorry, I couldn't find a relevant answer. Try rephrasing.",
            "links": []
        }

    # Extract context and links
    context = "\n\n".join([doc.page_content for doc in docs])
    links = [{"url": doc.metadata.get("source", ""), "text": doc.metadata.get("source", "")} for doc in docs]

    # LLM prompt
    prompt = f"""
You are a helpful TA for the TDS course at IITM Online.
Answer the student's question using the context below.

Context:
{context}

Question: {data.question}
Answer:
"""

    # Send to Ollama (LLaMA 3)
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False}
        )
        result = res.json()
        final_answer = result.get("response", "⚠️ No answer generated.")
    except Exception as e:
        final_answer = f"⚠️ Failed to generate answer: {str(e)}"

    return {
        "answer": final_answer.strip(),
        "links": links
    }

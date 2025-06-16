from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama  # for local LLaMA

# Initialize FastAPI
app = FastAPI()

# Root route for health check / deployment validation
@app.get("/")
async def root():
    return {"message": "✅ TDS Virtual TA is running. Visit /docs for API usage."}

# Load embeddings & FAISS index
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

# LLM setup (LLaMA via Ollama or comment this to use mock instead)
llm = ChatOllama(model="llama3")  # Ensure you’ve run `ollama pull llama3`

# Request schema
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

# POST endpoint for answering student questions
@app.post("/api/")
async def get_response(data: QueryInput):
    # Search top 3 similar chunks
    docs = db.similarity_search(data.question, k=3)

    if not docs:
        return {
            "answer": "❌ Sorry, I couldn't find a relevant answer. Try rephrasing.",
            "links": []
        }

    # Prepare context and links
    context = "\n\n".join([doc.page_content for doc in docs])
    links = [
        {"url": doc.metadata.get("source", ""), "text": doc.metadata.get("source", "")}
        for doc in docs
    ]

    # Prompt template
    prompt = PromptTemplate.from_template("""
You are a helpful Virtual TA for the TDS course.
Use the following context to answer the student's question.

Context:
{context}

Question:
{question}

Answer:
""")

    # Generate response from LLM
    try:
        final_answer = llm.invoke(
            prompt.format(context=context, question=data.question)
        ).strip()
    except Exception as e:
        final_answer = f"⚠️ LLM Error: {str(e)}"

    return {
        "answer": final_answer,
        "links": links
    }

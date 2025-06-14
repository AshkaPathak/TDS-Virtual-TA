import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set up CORS (optional, useful if connecting to frontend)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize embedding model
embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE")
)

# Load FAISS vector store
db = FAISS.load_local("TDS_Project1_Data/faiss_index", embedding, allow_dangerous_deserialization=True)

# Set up LLM (gpt-3.5-turbo or any OpenAI-compatible model)
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE")
)

# Set up RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

# Define input format
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None  # Placeholder for future image input

# API endpoint
@app.post("/api/")
async def get_response(data: QueryInput):
    # Get LLM answer
    answer = qa_chain.run(data.question)

    # Get top 3 similar chunks for context/links
    docs = db.similarity_search(data.question, k=3)
    links = [{"url": doc.metadata.get("source", ""), "text": doc.metadata.get("source", "")} for doc in docs]

    return {
        "answer": answer,
        "links": links
    }

# Local dev server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

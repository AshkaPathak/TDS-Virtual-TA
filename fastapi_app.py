from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

app = FastAPI()

# ✅ Root endpoint for Render and health check
@app.get("/")
async def root():
    return {
        "message": "✅ TDS Virtual TA is running. Visit /docs for Swagger UI."
    }

# ✅ GET fallback for /api/ so the form doesn’t break
@app.get("/api/")
async def get_api_info():
    return {
        "message": "TDS Virtual TA backend is running. Use POST method with a question to get a response."
    }

# 🔧 Fallback LLM that gives dummy responses
class MockLLM:
    def invoke(self, prompt: str) -> str:
        return "🤖 This is a placeholder answer. Please run locally with a real LLM."

llm = MockLLM()

# 📦 Input schema
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

# ✅ POST /api endpoint for actual usage
@app.post("/api/")
async def get_response(data: QueryInput):
    # 🔁 Lazy loading to avoid OOM errors on startup
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

    docs = db.similarity_search(data.question)
    content = "\n\n".join([doc.page_content for doc in docs])

    prompt = PromptTemplate.from_template(
        "You're a helpful TA for the TDS course. Use the context below:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"
    )

    full_prompt = prompt.format(context=content, question=data.question)
    response = llm.invoke(full_prompt)

    return {"answer": response}

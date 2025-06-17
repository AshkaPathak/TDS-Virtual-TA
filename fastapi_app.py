from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

app = FastAPI()

# ✅ Root health check
@app.get("/")
async def root():
    return {"message": "TDS Virtual TA is running. Visit /docs for Swagger UI."}

# ✅ Required GET /api/ route for TDS form
@app.get("/api/")
async def api_status():
    return {"status": "ok"}

# 🔧 Mock LLM fallback
class MockLLM:
    def invoke(self, prompt: str) -> str:
        return "🤖 This is a placeholder answer. Please run locally with a real LLM."

llm = MockLLM()

class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

@app.post("/api/")
async def get_response(data: QueryInput):
    try:
        embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

        docs = db.similarity_search(data.question)
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = PromptTemplate.from_template(
            "You're a helpful TA for the TDS course. Use the context below:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"
        )

        response = llm.invoke(prompt.format(context=context, question=data.question))
        return {"answer": response}

    except Exception as e:
        return {"error": f"Failed to load vectorstore or generate response: {str(e)}"}

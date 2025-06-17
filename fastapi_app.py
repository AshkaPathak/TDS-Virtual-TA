from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

app = FastAPI()

# ✅ Health check root route
@app.get("/")
async def root():
    return {"message": "TDS Virtual TA is running. Visit /docs for Swagger UI."}

# ✅ GET route to pass TDS submission form (it uses GET on /api/)
@app.get("/api/")
async def api_get_check():
    return {"status": "ok", "message": "Backend is up and running. Use POST to query."}

# 🧠 Dummy LLM (replace with real one locally)
class MockLLM:
    def invoke(self, prompt: str) -> str:
        return "🤖 This is a placeholder answer. Run locally for real results."

llm = MockLLM()

# 📦 Request schema
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

# ✅ Actual POST API endpoint
@app.post("/api/")
async def get_response(data: QueryInput):
    try:
        embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

        docs = db.similarity_search(data.question)
        context = "\n\n".join(doc.page_content for doc in docs)

        prompt = PromptTemplate.from_template(
            "You're a helpful TA for the TDS course. Use the context below:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"
        )

        full_prompt = prompt.format(context=context, question=data.question)
        response = llm.invoke(full_prompt)
        return {"answer": response}

    except Exception as e:
        return {"error": f"Something went wrong: {str(e)}"}

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "✅ FastAPI is live on Vercel!"}

@app.get("/api/")
def get_info():
    return {"status": "ok", "message": "Use POST on /api/ with a question."}

class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

class MockLLM:
    def invoke(self, prompt: str) -> str:
        return "🤖 This is a placeholder answer. Run locally for real LLM responses."

llm = MockLLM()

@app.post("/api/")
def get_answer(data: QueryInput):
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

    docs = db.similarity_search(data.question)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = PromptTemplate.from_template(
        "You are a helpful TA for the TDS course. Use the context below:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"
    )
    full_prompt = prompt.format(context=context, question=data.question)

    response = llm.invoke(full_prompt)
    return {"answer": response}

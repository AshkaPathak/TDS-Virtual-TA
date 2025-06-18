from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

app = FastAPI()

# 🩺 Health check
@app.get("/")
async def root():
    return {"status": "ok"}

# 🛠 Input schema
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

# 📤 Output format
class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

# 🤖 Mock LLM fallback
class MockLLM:
    def invoke(self, prompt: str) -> str:
        return "🤖 This is a placeholder answer. Please run locally with a real LLM for full functionality."

llm = MockLLM()

# 🧠 Handle POST /
@app.post("/", response_model=AnswerResponse)
async def get_response(data: QueryInput):
    try:
        # Lazy load FAISS to avoid OOM errors
        embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

        docs = db.similarity_search(data.question, k=2)
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = PromptTemplate.from_template(
            "You're a helpful TA. Use the context below to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        )

        full_prompt = prompt.format(context=context, question=data.question)
        response = llm.invoke(full_prompt)

        return {
            "answer": response,
            "links": [
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in",
                    "text": "Relevant discussion on course Discourse forum."
                }
            ]
        }

    except Exception as e:
        return {
            "answer": "⚠️ Error processing your question.",
            "links": []
        }

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from langchain_community.vectorstores import FAISS

app = FastAPI()

# ✅ MockEmbedding wrapped to act as callable
class MockEmbeddingWrapper:
    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]

    def embed_query(self, text):
        return [0.1] * 1536

    def __call__(self, text):  # This line makes it work like a function
        return self.embed_query(text)

# ✅ Instantiate correctly
embedding = MockEmbeddingWrapper()

# ✅ Load FAISS index safely
db = FAISS.load_local(
    "faiss_index", 
    embedding, 
    allow_dangerous_deserialization=True
)




# ✅ Request schema
class QueryInput(BaseModel):
    question: str
    image: Optional[str] = None

# ✅ API route
@app.post("/api/")
async def get_response(data: QueryInput):
    docs = db.similarity_search(data.question, k=3)
    context = "\n".join([doc.page_content for doc in docs])
    links = [{"url": doc.metadata.get("source", ""), "text": doc.metadata.get("source", "")} for doc in docs]

    return {
        "answer": context,
        "links": links
    }

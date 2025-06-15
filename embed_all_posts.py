import json
import os
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ✅ Mock embedding class (no OpenAI needed)
class MockEmbedding:
    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]
    def embed_query(self, text):
        return [0.1] * 1536

# Load posts
with open("TDS_Project1_Data/discourse_posts.json", "r") as f:
    posts = json.load(f)

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
documents = []

for post in posts:
    text = post.get("content", "").strip()
    source = post.get("url", "")
    if not text:
        continue
    chunks = splitter.split_text(text)
    for chunk in chunks:
        documents.append(Document(page_content=chunk, metadata={"source": source}))

print(f"📄 Loaded {len(documents)} document chunks")

# ✅ Use mock embeddings
embedding = MockEmbedding()

# Save FAISS index locally
faiss_index = FAISS.from_documents(documents, embedding)
faiss_index.save_local("TDS_Project1_Data/faiss_index")

print("✅ FAISS index created using mock embeddings.")

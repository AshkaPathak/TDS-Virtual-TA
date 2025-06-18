# embed_and_build_index.py
import json
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

# Load your scraped posts
with open("discourse_posts.json", "r") as f:
    posts = json.load(f)

# Create document list
docs = []
for p in posts:
    content = p.get("content", "").strip()
    if content:
        docs.append(Document(page_content=content))

# Initialize embeddings
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create and save vector store
db = FAISS.from_documents(docs, embedding)
db.save_local("faiss_index")
print("✅ Built and saved faiss_index folder")

import json
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
import os

# ✅ Step 1: Load posts from JSON
with open("discourse_posts.json", "r") as f:
    posts = json.load(f)

# ✅ Step 2: Create list of LangChain Documents
docs = []
for post in posts:
    content = post.get("content", "").strip()
    if content:
        docs.append(Document(page_content=content))

print(f"✅ Loaded {len(docs)} posts for embedding.")

# ✅ Step 3: Load sentence transformer embeddings
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# ✅ Step 4: Generate FAISS index
db = FAISS.from_documents(docs, embedding)

# ✅ Step 5: Save index to faiss_index/
os.makedirs("faiss_index", exist_ok=True)
db.save_local("faiss_index")
print("✅ FAISS index saved to ./faiss_index")

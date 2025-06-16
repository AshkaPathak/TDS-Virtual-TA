import os
import json
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# 📁 1. Load Markdown documents
md_docs = []
md_path = "tds_pages_md"
for filename in os.listdir(md_path):
    if filename.endswith(".md"):
        loader = TextLoader(os.path.join(md_path, filename))
        md_docs.extend(loader.load())

# 📁 2. Load Discourse posts from JSON
json_docs = []
with open("TDS_Project1_Data/discourse_posts.json", "r") as f:
    data = json.load(f)
    for post in data:
        content = post.get("content", "")
        source = post.get("url", "")
        if content:
            json_docs.append(Document(page_content=content, metadata={"source": source}))

# ✅ 3. Combine documents
all_docs = md_docs + json_docs

# 🧩 4. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(all_docs)

# 🤖 5. Embed and save FAISS index
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(chunks, embedding)
db.save_local("faiss_index")

print(f"✅ Embedded and saved {len(chunks)} chunks from {len(all_docs)} sources.")

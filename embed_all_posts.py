import json
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Load posts
with open("TDS_Project1_Data/discourse_posts.json", "r") as f:
    posts = json.load(f)

documents = []
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

for post in posts:
    text = post.get("content", "").strip()
    source = post.get("url", "")
    
    if not text:
        print(f"⚠️ Skipping empty post: {source}")
        continue

    chunks = splitter.split_text(text)
    for chunk in chunks:
        documents.append(Document(page_content=chunk, metadata={"source": source}))

print(f"📄 Loaded {len(documents)} document chunks for embedding")

# ✅ CORRECT: Instantiate OpenAIEmbeddings properly
embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE")
)

# Generate FAISS index
faiss_index = FAISS.from_documents(documents, embedding)
faiss_index.save_local("TDS_Project1_Data/faiss_index")

print("✅ FAISS index created with IITM-proxy-based OpenAI embeddings.")

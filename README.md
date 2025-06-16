# TDS Virtual TA Project

Hi! I’m Ashka Pathak, and this is my **Virtual Teaching Assistant project** for the *Tools in Data Science (TDS)* course, built as part of the **IIT Madras Online BSc Data Science** program. This assistant is designed to:

- Scrape and store TDS course content
- Download Discourse forum posts with authentication
- Respond to student queries via a lightweight API

This project reflects my hands-on learning in web scraping, API development, and automation. It was both challenging and rewarding—and it greatly deepened my understanding of backend systems and data structuring.

[Live Demo](https://tds-virtual-ta-446g.onrender.com) — Try it out using the Swagger UI

## What I Learned

This project challenged me to apply:
- **Web scraping** (static + session-based)
- **Embedding-based search** using FAISS
- **API design and testing** with FastAPI + Swagger
- **Mocking embeddings** when OpenAI wasn't available
  
## Overview

This repository includes:

1. A **website scraper** that collects TDS course pages in Markdown format
2. A **Discourse post downloader** with session-based authentication
3. A **FastAPI server** that processes student queries and generates responses

## Project Structure
```bash
.
├── discourse_posts.json             # Combined Discourse data
├── discourse_json/                  # Topic-wise JSON dumps
├── tds_pages_md/                    # Markdown pages of the course site
├── TDS_Project1_Data/               # Code for scraping and downloading
│   ├── discourse_scraper.py
│   ├── website_downloader_full.py
│   ├── tds_discourse_downloader.py
│   └── ...
├── fastapi_app.py                   # FastAPI server with mock embeddings
├── embed_all_posts.py               # Generates FAISS index
├── faiss_index/                     # Stored FAISS vectorstore (index.faiss, index.pkl)
├── requirements.txt                 # Python dependencies
├── Procfile                         # Render deployment entrypoint
└── README.md
```

## Features

1. Automatically scrapes **TDS course content** from the official website into markdown
2. Downloads all **Discourse forum posts** from Jan 1 to Apr 14, 2025 using cookies authentication
3. Implements a **FastAPI backend** for query handling and answers the questions using **FAISS vector search** over scraped content
4. Deploys with **Render** for public access

## Installation
1. **Clone and set up**
   ```bash
   git clone https://github.com/AshkaPathak/TDS-Virtual-TA.git
   cd TDS-Virtual-TA
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
    ```
2. **Scrape the course content**
   ```bash
   python TDS_Project1_Data/website_downloader_full.py
   ```
   
3. **Download discourse posts**
   ```bash
   python TDS_Project1_Data/website_downloader_full.py
   ```
   **!!**Requires auth.json with cookie header string

4. **Generate embeddings (FAISS)**
   ```bash
   python embed_all_posts.py
   ```
   
5. **Start API server**
   ```bash
   uvicorn fastapi_app:app --reload
   ```
   Go to: http://localhost:8000/docs
   
## Deployed Version
You can access the hosted version here:
https://tds-virtual-ta-446g.onrender.com

## Data Structure

- discourse_posts.json – Full Discourse post dump
- discourse_json/ – Individual JSON files per topic
- tds_pages_md/ – Markdown-formatted course pages

## License

This project is licensed under the MIT License.

## Notes & Reflections

Handling dynamic content was challenging, especially when facing JSON decoding issues. I later explored tools like Playwright for session-based scraping. Rather than copying code blindly, I tested and customized each component to ensure I fully understood how web scraping, data formatting, and API routing work together.

To download authenticated Discourse posts, I manually extracted cookies from the browser using DevTools. This required me to explore various DevTools tabs (Elements, Application, etc.), helping me understand session management, HTTP headers, and browser storage. Whereas for deployment, I used mock embeddings to avoid OpenAI dependencies which led me to implementing a MockEmbeddingWrapper that mimicked embed_documents() and embed_query()—this involved making the class callable and compatible with FAISS’s expectations.

I faced certain challenges while debugging FAISS paths such as the file not found errors. Since FAISS doesn’t provide user-friendly error messages, so debugging "FileIOReader failed" involved a lot of trial and error—checking whether files were committed properly, inside the correct subfolders, and accessible via the deployment path. I also leanred how FAISS uses binary serialization (such as index.faiss for vectors and index.pkl for metadata). Knowing the difference between serialized index data and associated metadata helped me ensure both files were loaded correctly and mapped back into langchain's vector store structure.

## Related Links

[TDS 2025-01 Website](https://tds.s-anand.net/#/2025-01/)

[TDS Discourse Forum](https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34)

[My GitHub Profile](https://github.com/AshkaPathak)

# TDS Virtual TA Project

Hi! I’m Ashka Pathak, and this is my **Virtual Teaching Assistant project** for the *Tools in Data Science (TDS)* course, built as part of the **IIT Madras Online BSc Data Science** program. This assistant is designed to:

- Scrape and store TDS course content
- Download Discourse forum posts with authentication
- Respond to student queries via a lightweight API

This project reflects my hands-on learning in web scraping, API development, and automation. It was both challenging and rewarding—and it greatly deepened my understanding of backend systems and data structuring.

[Live Demo](https://tds-virtual-ta-446g.onrender.com) — Try it out using the Swagger UI

## What I Learned

This project challenged me to apply:
- How to structure and scrape real-world educational content
- How to use browser cookies for session-based authenticated downloads
- How FAISS works internally: binary .faiss for embeddings and .pkl for metadata
- How to mock embeddings when OpenAI wasn’t usable
- How to deploy using Render + manage vectorstores in production

## Overview

This repository includes:

1. A **website scraper** that collects TDS course pages in Markdown format
2. A **Discourse post downloader** with session-based authentication
3. A **FastAPI server** that processes student queries and generates responses

## Project Structure
```bash
.
├── discourse_posts.json               # Combined Discourse data
├── discourse_json/                    # Topic-wise JSON dumps
├── tds_pages_md/                      # Markdown pages of the course site
├── TDS_Project1_Data/                 # Code for scraping and downloading
│ ├── discourse_scraper.py
│ ├── website_downloader_full.py
│ ├── tds_discourse_downloader.py
│ └── ...
├── fastapi_app.py                     # FastAPI server with LLM response generation
├── embed_all_posts.py                 # Generates FAISS index
├── faiss_index/                       # Stored FAISS vectorstore (index.faiss, index.pkl)
├── requirements.txt                   # Python dependencies
├── Procfile                           # Render deployment entrypoint
└── README.md
```

## Features

1. Automatically scrapes **TDS course content** from the official website into markdown
2. Downloads all **Discourse forum posts** from Jan 1 to Apr 14, 2025 using cookies authentication
3. Implements a **FastAPI backend** for query handling and answers the questions using **FAISS vector search** over scraped content
4. Responds to questions using either OpenAI or local LLM (LLaMA)
5. Runs a FastAPI server with a REST API

## Installation
1. **Clone and create a virtual environment**
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
   
3. **Download discourse posts (requires cookies)** 
   ```bash
   python TDS_Project1_Data/tds_discourse_downloader.py
   ```

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
You can access the hosted version [here](tds-virtual-ta-446g.onrender.com)

## Data Format

- discourse_posts.json – Full Discourse post dump
- discourse_json/ – Individual JSON files per topic
- tds_pages_md/ – Markdown-formatted course pages

## License

This project is licensed under the MIT License.

## Notes & Reflections

---

## 📓 Notes & Reflections

This wasn’t just a regular course project—it genuinely pushed me to explore real-world tools beyond theory.

Firstly, I didn’t have access to a personal OpenAI key, so I had to mock the embedding system to get things running. Figuring out how `FAISS` expects `embed_documents()` and `embed_query()` gave me a solid look into how LangChain works under the hood.
 
FAISS gave me a hard time. Especially when the index wouldn’t load and all I got was a vague "FileIOReader failed" error. Turns out you need both `index.faiss` (the actual vectors) and `index.pkl` (the metadata) properly placed and committed—learnt that the hard way.

Moreover, downloading discourse posts wasn’t straightforward. Digging through Chrome DevTools, figure out which cookies to grab, and pass them correctly in the header is a good way to go I learned. Just because of this project, I learned more about headers, sessions, and auth than in any previous scraping work.
 
FastAPI + Swagger UI made testing fun. Seeing the API work live and actually respond to queries felt super rewarding after all the backend pieces came together.

Running LLaMA 3 locally via Ollama was a great fallback. It made me realize how far open-source models have come. It was slower, but it worked—and that gave me the confidence to say: this project doesn’t *need* OpenAI to run.

Right when I thought this is finally going well, I accidentally committed the entire `venv/`, hit GitHub’s file size limit, and had to use `git filter-repo` to clean it up. Annoying at the time, but now I know how to keep my Git history clean and lightweight.

This whole process helped me connect scraping, embeddings, APIs, and deployment into one working pipeline. It wasn’t smooth, but it was worth it.

## Related Links

[TDS 2025-01 Website](https://tds.s-anand.net/#/2025-01/)

[TDS Discourse Forum](https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34)

[My GitHub Profile](https://github.com/AshkaPathak)

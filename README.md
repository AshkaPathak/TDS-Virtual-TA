# TDS Virtual TA Project

Hi! I’m Ashka Pathak, and this is my **Virtual Teaching Assistant project** for the *Tools in Data Science (TDS)* course, built as part of the **IIT Madras Online BSc Data Science** program. This assistant is designed to:

- Scrape and store TDS course content
- Download Discourse forum posts with authentication
- Respond to student queries via a lightweight API

This project reflects my hands-on learning in web scraping, API development, and automation. It was both challenging and rewarding—and it greatly deepened my understanding of backend systems and data structuring.

## Overview

This repository includes:

1. A **website scraper** that collects TDS course pages in Markdown format
2. A **Discourse post downloader** with session-based authentication
3. A **FastAPI server** that processes student queries and generates responses

## Project Structure
```bash
..
├── discourse_posts.json            # Consolidated Discourse data
├── discourse_json/                 # Individual topic-wise Discourse JSONs
├── tds_pages_md/                   # Markdown pages for course content
├── tds_discourse_downloader.py     # Script to download Discourse posts
├── website_downloader_full.py      # Script to download TDS website pages
├── api/
│ └── main.py                       # FastAPI server app
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## Features

1. Automatically scrapes **TDS course content** from the official website
2. Downloads all **Discourse forum posts** from Jan 1 to Apr 14, 2025 using cookies
3. Implements a **FastAPI backend** for query handling
4. Customizable and runs locally on any machine

## Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/AshkaPathak/TDS-Virtual-TA.git
   cd TDS-Virtual-TA
    ```
   
2. **Set up a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   
## Usage

### Download website content
```bash
python website_downloader_full.py
```
Stores TDS Jan 2025 content up to 15 Apr 2025.

### Download Discourse posts
```bash
python tds_discourse_downloader.py
``` 
Downloads all posts between Jan 1 and Apr 14, 2025 using authentication cookies.

### Run the FastAPI server
```bash
uvicorn api.main:app --reload
```

## Data Structure

- discourse_posts.json – Full Discourse post dump
- discourse_json/ – Individual JSON files per topic
- tds_pages_md/ – Markdown-formatted course pages

## License

This project is licensed under the MIT License.

## Notes & Reflections

To download authenticated Discourse posts, I manually extracted cookies from the browser using DevTools. This required me to explore various DevTools tabs (Elements, Application, etc.), helping me understand session management, HTTP headers, and browser storage.

Handling dynamic content was challenging, especially when facing JSON decoding issues. I later explored tools like Playwright for session-based scraping. Rather than copying code blindly, I tested and customized each component to ensure I fully understood how web scraping, data formatting, and API routing work together.

## Related Links

[TDS 2025-01 Website](https://tds.s-anand.net/#/2025-01/)
[TDS Discourse Forum](https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34)
[My GitHub Profile](https://github.com/AshkaPathak)

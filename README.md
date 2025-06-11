# TDS Virtual TA Project

Hi! I’m Ashka Pathak, and this is my Tools in Data Science (TDS) Virtual Teaching Assistant project, created as part of the IIT Madras Online Degree program. It’s designed to scrape course content and download Discourse posts for the TDS course—and then use that data to answer student questions via a simple API.

This project reflects my own learning journey in web scraping, API development, and automation. It’s been a challenging but rewarding experience, and I’ve learned a lot along the way!

## Overview

This repository includes:

1. A website scraper that collects TDS course pages in Markdown format.
2. A Discourse post downloader that collects posts from the official Discourse forum (with proper authentication).
3. A FastAPI backend that takes student questions and responds using the scraped data.

## Project Structure
```bash
.
├── discourse_posts.json          # JSON file with Discourse posts data
├── discourse_json/               # Directory with individual topic JSON files
├── tds_pages_md/                 # Markdown files for each TDS course page
├── tds_discourse_downloader.py   # Script to download Discourse posts
├── website_downloader_full.py    # Script to download website pages
├── api/                          # API server code
│   └── main.py                   # FastAPI app
├── requirements.txt              # Required Python packages
└── README.md                     # This file
```

## Features

1. Scrapes TDS course content automatically
2. Downloads all Discourse posts within a date range using cookies
3. Exposes a FastAPI endpoint to handle student queries
4. Easy to run locally on any system

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AshkaPathak/TDS-Project1-Data.git
   cd TDS-Project1-Data
    ```

2. **Set up the virtual environment**
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
stores all the current content for TDS Jan 2025 till 15 Apr 2025.

### Download Discourse posts
```bash
python tds_discourse_downloader.py
``` 
is used to download all the discourse posts and its details raning from the date 1 Jan 2025  to 14 Apr 2025.

### Run the API
```bash
uvicorn api.main:app --reload
```
## Data Structure

**discourse_posts.json**: Consolidated JSON of all posts.
**discourse_json/**: Individual JSON files for each topic.
**tds_pages_md/**: Markdown files containing course pages.

## License

This project is licensed under the MIT License.

## Notes & Reflections

I manually created the cookie string required for authenticated Discourse scraping by inspecting the website. This part was tricky since I was using the inspect section further contains a lot more sections such as elements, sources, applications. This allowed me to explore a lot about session management and HTTP requests. Furthermore, I encountered several challenges with handling dynamic content (like JSON decoding errors) and then learned about Playwright which make session-based scraping much easier. I deliberately customized and tested all scripts instead of simply copying, to ensure that I understand each step in the scraping process and API development.

## Related Links

[TDS 2025-01 Website] (https://tds.s-anand.net/#/2025-01/)
[TDS Discourse Forum] (https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34)
[My GitHub Profile] (https://github.com/AshkaPathak)
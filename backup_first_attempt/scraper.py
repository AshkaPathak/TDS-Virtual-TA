from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

def scrape_course():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get("https://tds.s-anand.net/")
    time.sleep(2)

    sidebar_links = driver.find_elements(By.CSS_SELECTOR, "aside.sidebar-nav a.section-link, aside.sidebar-nav > ul > li > a")
    entries = []

    for link in sidebar_links:
        href = link.get_attribute("href")
        title = link.get_attribute("title") or link.text.strip()
        if not href or href.startswith("javascript:"):
            continue
        driver.get(href)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        content_div = soup.find("article", {"class": "markdown-section"})
        text = content_div.get_text(separator="\n").strip() if content_div else ""
        entries.append({"title": title, "url": href, "content": text})

    driver.quit()
    return entries

if __name__ == "__main__":
    data = scrape_course()
    with open("course_content.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} sections.")

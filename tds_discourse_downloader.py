import os
import json
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError
from bs4 import BeautifulSoup

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_ID = 34
CATEGORY_JSON_URL = f"{BASE_URL}/c/courses/tds-kb/{CATEGORY_ID}.json"
AUTH_STATE_FILE = "auth.json"
DATE_FROM = datetime(2025, 1, 1)
DATE_TO = datetime(2025, 4, 15)

def parse_date(date_str):
    """Convert date strings from Discourse to datetime objects."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

def manual_login(playwright):
    """Prompt the user to login manually and save auth state."""
    print("Login required. Opening browser...")
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{BASE_URL}/login")
    print("Please complete the login manually, then press Resume in Playwright.")
    page.pause()
    context.storage_state(path=AUTH_STATE_FILE)
    print("Authentication saved successfully.")
    browser.close()

def check_authentication(page):
    """Verify if stored authentication works by fetching a known page."""
    try:
        page.goto(CATEGORY_JSON_URL, timeout=10000)
        page.wait_for_selector("pre", timeout=5000)
        json.loads(page.inner_text("pre"))
        return True
    except (TimeoutError, json.JSONDecodeError):
        return False

def fetch_and_save_posts(playwright):
    """Fetch posts from Discourse using stored authentication."""
    print("Starting data collection using saved session.")
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(storage_state=AUTH_STATE_FILE)
    page = context.new_page()
    all_topics = []
    page_num = 0

    while True:
        paginated_url = f"{CATEGORY_JSON_URL}?page={page_num}"
        print(f"Fetching page {page_num}...")
        page.goto(paginated_url)
        try:
            data = json.loads(page.inner_text("pre"))
        except Exception:
            data = json.loads(page.content())

        topics = data.get("topic_list", {}).get("topics", [])
        if not topics:
            break

        all_topics.extend(topics)
        page_num += 1

    print(f"Collected {len(all_topics)} topics.")

    collected_posts = []
    for topic in all_topics:
        created_at = parse_date(topic["created_at"])
        if DATE_FROM <= created_at <= DATE_TO:
            topic_url = f"{BASE_URL}/t/{topic['slug']}/{topic['id']}.json"
            page.goto(topic_url)
            try:
                topic_data = json.loads(page.inner_text("pre"))
            except Exception:
                topic_data = json.loads(page.content())

            posts = topic_data.get("post_stream", {}).get("posts", [])
            accepted_answer_id = topic_data.get("accepted_answer_post_id")

            reply_counter = {}
            for post in posts:
                reply_to = post.get("reply_to_post_number")
                if reply_to is not None:
                    reply_counter[reply_to] = reply_counter.get(reply_to, 0) + 1

            for post in posts:
                post_entry = {
                    "topic_id": topic["id"],
                    "topic_title": topic.get("title"),
                    "category_id": topic.get("category_id"),
                    "tags": topic.get("tags", []),
                    "post_id": post["id"],
                    "post_number": post["post_number"],
                    "author": post["username"],
                    "created_at": post["created_at"],
                    "updated_at": post.get("updated_at"),
                    "reply_to_post_number": post.get("reply_to_post_number"),
                    "is_reply": post.get("reply_to_post_number") is not None,
                    "reply_count": reply_counter.get(post["post_number"], 0),
                    "like_count": post.get("like_count", 0),
                    "is_accepted_answer": post["id"] == accepted_answer_id,
                    "mentioned_users": [u["username"] for u in post.get("mentioned_users", [])],
                    "url": f"{BASE_URL}/t/{topic['slug']}/{topic['id']}/{post['post_number']}",
                    "content": BeautifulSoup(post["cooked"], "html.parser").get_text()
                }
                collected_posts.append(post_entry)

    with open("discourse_posts.json", "w", encoding="utf-8") as f:
        json.dump(collected_posts, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(collected_posts)} posts from {DATE_FROM.date()} to {DATE_TO.date()}.")
    browser.close()

def main():
    with sync_playwright() as p:
        if not os.path.exists(AUTH_STATE_FILE):
            manual_login(p)
        else:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(storage_state=AUTH_STATE_FILE)
            page = context.new_page()
            if not check_authentication(page):
                print("Session expired. Please log in again.")
                browser.close()
                manual_login(p)
            else:
                print("Authentication confirmed.")
                browser.close()

        fetch_and_save_posts(p)

if __name__ == "__main__":
    main()

    
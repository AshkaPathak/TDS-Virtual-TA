import requests
import os
import json
from datetime import datetime, timezone
from urllib.parse import urljoin

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in/"
CATEGORY_SLUG = "courses/tds-kb"
CATEGORY_ID = 34
START_DATE = "2025-01-01"
END_DATE = "2025-04-15"

COOKIE_STRING = (
    "_forum_session=AAzQlNY43ZPNSC61Y1FeVyanOUgooVpldetOgKnoks6EeVSDbbfiYYe75bgus4P5T0YFyW1YsRgdHDhY2hoGfsjOJHLADzzYiDpmM..."
    "_t=nnpqKZq2Ejfz0Rk3nB8Z%2BRxb5SMR0UYTK0aARmc9xyKZMGR%2BbDsMN92Ppc023wiUgJNjnWqyLdXTolnhw7HvjBbJEuZWTDF8bNUNID3ctpT..."
    "_bypass_cache=true"
)
OUTPUT_DIR = "discourse_json"
POSTS_BATCH_SIZE = 50
MAX_EMPTY_PAGES = 5

def extract_cookies(cookie_str):
    cookies = {}
    for part in cookie_str.strip().split(";"):
        if "=" in part:
            key, value = part.strip().split("=", 1)
            cookies[key] = value
    return cookies

def fetch_topic_ids(base_url, slug, category_id, start, end, cookies):
    url = urljoin(base_url, f"c/{slug}/{category_id}.json")
    collected_ids = []
    page = 0
    no_new_topics_count = 0
    previous_count = 0

    start_dt = datetime.fromisoformat(start + "T00:00:00").replace(tzinfo=timezone.utc)
    end_dt = datetime.fromisoformat(end + "T23:59:59.999999").replace(tzinfo=timezone.utc)

    print(f"Fetching topics from {start_dt} to {end_dt}")

    while True:
        try:
            response = requests.get(f"{url}?page={page}", cookies=cookies, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

        topics = data.get("topic_list", {}).get("topics", [])
        if not topics:
            print(f"No more topics found on page {page}.")
            break

        before_count = len(set(collected_ids))
        for topic in topics:
            created = topic.get("created_at")
            if created:
                try:
                    created_date = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    if start_dt <= created_date <= end_dt:
                        collected_ids.append(topic["id"])
                except ValueError:
                    print(f"Skipping invalid date format in topic {topic.get('id')}")

        current_count = len(set(collected_ids))
        if current_count == before_count:
            no_new_topics_count += 1
        else:
            no_new_topics_count = 0

        if no_new_topics_count >= MAX_EMPTY_PAGES:
            print(f"Reached {MAX_EMPTY_PAGES} consecutive pages without new topics. Stopping.")
            break

        page += 1

    print(f"Found {len(set(collected_ids))} unique topics.")
    return list(set(collected_ids))

def fetch_topic_details(base_url, topic_id, cookies):
    url = urljoin(base_url, f"t/{topic_id}.json")
    try:
        response = requests.get(url, cookies=cookies, timeout=30)
        response.raise_for_status()
        topic_data = response.json()
    except Exception as e:
        print(f"Failed to fetch topic {topic_id}: {e}")
        return None

    posts = topic_data.get("post_stream", {}).get("stream", [])
    loaded_posts = {post["id"] for post in topic_data.get("post_stream", {}).get("posts", [])}
    missing_posts = [pid for pid in posts if pid not in loaded_posts]

    if missing_posts:
        print(f"Topic {topic_id} missing {len(missing_posts)} posts. Fetching additional batches.")
        additional_posts = []
        for i in range(0, len(missing_posts), POSTS_BATCH_SIZE):
            batch_ids = missing_posts[i:i + POSTS_BATCH_SIZE]
            batch_url = urljoin(base_url, f"t/{topic_id}/posts.json")
            try:
                resp = requests.get(batch_url, params=[("post_ids[]", pid) for pid in batch_ids], cookies=cookies, timeout=60)
                resp.raise_for_status()
                batch_data = resp.json()
                additional_posts.extend(batch_data.get("post_stream", {}).get("posts", []))
            except Exception as e:
                print(f"Failed to fetch batch posts for topic {topic_id}: {e}")

        if additional_posts:
            topic_data["post_stream"]["posts"].extend(additional_posts)

    return topic_data

def save_topic_data(topic_id, data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"topic_{topic_id}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f" Could not save topic {topic_id}: {e}")

def main():
    print("Starting Discourse Scraper")
    cookies = extract_cookies(COOKIE_STRING)

    topic_ids = fetch_topic_ids(BASE_URL, CATEGORY_SLUG, CATEGORY_ID, START_DATE, END_DATE, cookies)
    if not topic_ids:
        print("No topics found. Exiting.")
        return

    success_count = 0
    for idx, topic_id in enumerate(topic_ids, 1):
        print(f"[{idx}/{len(topic_ids)}] Fetching topic {topic_id}")
        data = fetch_topic_details(BASE_URL, topic_id, cookies)
        if data:
            save_topic_data(topic_id, data, OUTPUT_DIR)
            success_count += 1

    print(f"Completed! {success_count}/{len(topic_ids)} topics saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()

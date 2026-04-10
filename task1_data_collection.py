import requests
import time
import os
from datetime import datetime
import json

categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

LIMIT = 25

headers = {"User-Agent": "TrendPulse/1.0"}



print(" Hacker News!")

url_list = "https://hacker-news.firebaseio.com/v0/topstories.json"


response = requests.get(url_list, headers=headers)


if response.status_code != 200:
    print(" The library door is closed.")
    exit()


story_ids = response.json()

story_ids = story_ids[:500]

print(f" Found {len(story_ids)} story IDs.  start sorting!")

all_collected_stories = []


category_counts = {cat: 0 for cat in categories}

checked_ids = set()


for category_name in categories:

    print(f"\n Looking for '{category_name}' stories...")


    found_in_this_category = 0


    keywords = categories[category_name]


    for story_id in story_ids:

        if found_in_this_category >= LIMIT:
            break

        if story_id in checked_ids:
            continue


        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

        try:

            story_resp = requests.get(story_url, headers=headers)


            if story_resp.status_code != 200:
                continue

            story_data = story_resp.json()

            if not story_data or "title" not in story_data:
                continue

            title = story_data.get("title", "")
            title_lower = title.lower()


            is_match = False
            for word in keywords:

                if word in title_lower:
                    is_match = True
                    break


            if is_match:

                checked_ids.add(story_id)


                story_report = {
                    "post_id": story_data.get("id"),
                    "title": title,
                    "category": category_name,
                    "score": story_data.get("score"),
                    "num_comments": story_data.get("descendants", 0),
                    "author": story_data.get("by"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }


                all_collected_stories.append(story_report)
                found_in_this_category += 1
                print(f" Found one! ({found_in_this_category}/25): {title[:30]}...")

        except Exception as e:

            print(f" Error checking story {story_id}. Moving on.")
            continue
    print(f" Finished '{category_name}'. Taking a 2 second nap...")
    time.sleep(2)



if not os.path.exists("data"):
    os.makedirs("data")
    print(" Created a new folder named 'data'.")


today_date = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{today_date}.json"


with open(filename, "w") as f:
    json.dump(all_collected_stories, f, indent=2)


total_count = len(all_collected_stories)
print("\n" + "="*40)
print(f" SUCCESS!")
print(f"Collected {total_count} stories.")
print(f"Saved to {filename}")
print("="*40)
"""
 Habitica Task Importer v2
-------------------------------------------------
Imports Habits, Dailies, To-Dos, and Rewards from a JSON file into your Habitica account
and automatically creates tags with valid UUIDs if they don't already exist.

⚙️ Requirements:
    pip install requests

🔑 Before running:
    - Go to Habitica → Settings → API → copy your User ID and API Token.
    - Paste them into USER_ID and API_TOKEN below.
    - Ensure the JSON file is in the same directory.
"""

import json
import requests
import os
from time import sleep
import sys
sys.stdout.reconfigure(encoding='utf-8')

# === 1. CONFIGURE YOUR CREDENTIALS ===
USER_ID = "your-user-id"
API_TOKEN = "your-api-token"
JSON_FILE = "habitica_tasks.json"

# === 2. API SETUP ===
API_BASE = "https://habitica.com/api/v3"
HEADERS = {
    "x-api-user": USER_ID,
    "x-api-key": API_TOKEN,
    "x-client": "user-habiticaImportScript",
    "Content-Type": "application/json"
}

# === 3. TAG HELPERS ===
def get_existing_tags():
    """Fetch all existing tags from Habitica."""
    response = requests.get(f"{API_BASE}/tags", headers=HEADERS)
    if response.status_code == 200:
        tags = {t["name"]: t["id"] for t in response.json()["data"]}
        print(f"📘 Found {len(tags)} existing tags.")
        return tags
    else:
        print(f"⚠️ Could not fetch existing tags: {response.status_code} -> {response.text}")
        return {}

def create_tag(tag_name):
    """Create a new tag and return its UUID."""
    response = requests.post(f"{API_BASE}/tags", headers=HEADERS, json={"name": tag_name})
    if response.status_code == 201:
        tag_id = response.json()["data"]["id"]
        print(f"🏷️ Created tag: {tag_name}")
        return tag_id
    else:
        print(f"⚠️ Failed to create tag '{tag_name}': {response.text}")
        return None

def ensure_tags(tag_list, existing_tags):
    """Ensure all tags exist and return their UUID list."""
    tag_ids = []
    for tag in tag_list:
        if tag in existing_tags:
            tag_ids.append(existing_tags[tag])
        else:
            new_id = create_tag(tag)
            if new_id:
                existing_tags[tag] = new_id
                tag_ids.append(new_id)
    return tag_ids

# === 4. IMPORT FUNCTION ===
def import_tasks():
    try:
        if not os.path.exists(JSON_FILE):
            print(f"❌ File not found: {JSON_FILE}")
            return

        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        tasks = data.get("data", {}).get("tasks", [])
        print(f"📦 Found {len(tasks)} tasks in {os.path.basename(JSON_FILE)}")

        # Fetch tags first
        existing_tags = get_existing_tags()
        created_tags = {}
        successful_tasks = 0

        for i, task in enumerate(tasks, start=1):
            # Map tag names to real UUIDs
            if "tags" in task and isinstance(task["tags"], list):
                task["tags"] = ensure_tags(task["tags"], existing_tags)
                for k, v in existing_tags.items():
                    created_tags[k] = v

            # Clean unsupported fields
            task.pop("difficulty_label", None)
            # Send POST request to Habitica API
            response = requests.post(f"{API_BASE}/tasks/user", headers=HEADERS, json=task)
            if response.status_code == 201:
                print(f"✅ [{i}/{len(tasks)}] Added: {task['text']}")
                successful_tasks += 1
            else:
                print(f"⚠️ [{i}/{len(tasks)}] Failed: {task['text']} ({response.status_code}) -> {response.text}")

            sleep(1.1)  # avoid rate limiting

        print(f"\n🎉 {successful_tasks} / {len(tasks)} + Import complete! Check your Habitica dashboard.")
        if created_tags:
            print("\n📜 Tag Summary:")
            for name, tag_id in created_tags.items():
                print(f"  • {name}: {tag_id}")

    except Exception as e:
        print("❌ Error:", e)

# === 5. RUN ===
if __name__ == "__main__":
    import_tasks()

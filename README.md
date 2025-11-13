# 🕯️ Habitica Task Importer v2

A Python utility to import **Habits**, **Dailies**, **To-Dos**, and **Rewards** from a JSON file into your [Habitica](https://habitica.com) account.  
It automatically creates missing **tags with valid UUIDs** and assigns them to your tasks.

---

## ⚙️ Requirements

- **Python 3.7+**
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

---

## 🔑 Setup

1. **In Habitica:**
   - Go to **Settings → API**
   - Copy your **User ID** and **API Token**

2. **Open `habiticaImport.py`** and set:
   ```python
   USER_ID = "your-user-id"
   API_TOKEN = "your-api-token"
   JSON_FILE = "habitica_tasks.json"
   ```

3. **Folder structure (Make sure to use this layout):**
   ```bash
   habitica-importer/
   │
   ├── habiticaImport.py           # Main importer script
   ├── habitica_tasks.json         # JSON file to import (see example below)
   ├── requirements.txt
   └── README.md
   ```

4. **Run the importer:**
   ```bash
   python habiticaImport.py
   ```

---

## 📁 JSON File Example

Here’s what your `habitica_tasks.json` should look like:

```json
{
  "version": 3,
  "data": {
    "tasks": [
      {
        "text": "🧩 Code Practice Ritual",
        "type": "daily",
        "notes": "Solve 1–2 coding problems",
        "priority": 1.5,
        "attribute": "int",
        "tags": ["Coding", "Skill", "🪴"],
        "repeat": {"m": true, "t": true, "w": true, "th": true, "f": true, "s": true, "su": true},
        "startDate": "2025-10-19",
        "checklist": [
          {"text": "🔍 Stage I: Problem Hunt"},
          {"text": "🛠️ Stage II: Code Ritual"},
          {"text": "🪞 Stage III: Reflection"}
        ]
      },
      {
        "text": "📖 Lore Tome",
        "type": "reward",
        "notes": "Buy a book or course related to your field",
        "value": 120,
        "tags": ["RewardShop"]
      }
    ]
  }
}
```

### 🔍 Field Reference

| Field | Description |
|-------|--------------|
| `text` | Task name (appears in Habitica) |
| `type` | Task type: `habit`, `daily`, `todo`, or `reward` |
| `notes` | Optional description or notes |
| `priority` | Task difficulty (0.1 = Trivial, 1 = normal, 1.5 = hard, 2 = very hard) |
| `attribute` | Stat affected (`str`, `int`, `con`, `per`) |
| `tags` | List of tag names (created automatically if missing) |
| `repeat` | Which weekdays the daily repeats on |
| `startDate` | Start date in `YYYY-MM-DD` format |
| `checklist` | Optional checklist items |
| `value` | For rewards: gold cost to buy it |

---

## 🧩 Features

- Imports Habits, Dailies, To-Dos, and Rewards  
- Automatically creates tags if missing  
- Handles Habitica’s rate limits safely  
- Prints a summary of created tags and results  

---

## 🪄 Example Output

```
📦 Found 12 tasks in habitica_path.json
📘 Found 5 existing tags.
🏷️ Created tag: Study
✅ [1/12] Added: Morning Routine
✅ [2/12] Added: Write Code
...
🎉 12/12 Import complete! Check your Habitica dashboard.
```

---

## ⚠️ Notes

- 🚫 Do **not** share your API token publicly.  
- 🕐 The script already waits ~1.1 seconds per request to respect Habitica’s rate limits.  
- 🧪 For safety, test first using a temporary Habitica account.  

---

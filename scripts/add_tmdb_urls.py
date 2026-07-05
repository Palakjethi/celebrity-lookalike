import json
import os
import requests
import time
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
META_PATH = "models/meta.json"

session = requests.Session()
retry = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)

with open(META_PATH, "r") as f:
    metadata = json.load(f)

print(f"Adding TMDB photo URLs for {len(metadata)} celebrities...")

for i, celeb in enumerate(metadata):
    if celeb.get("tmdb_photo_url"):
        continue

    name = celeb["name"]
    try:
        # search for person on TMDB
        res = session.get(
            "https://api.themoviedb.org/3/search/person",
            params={"api_key": API_KEY, "query": name},
            timeout=10
        )
        results = res.json().get("results", [])
        if results and results[0].get("profile_path"):
            path = results[0]["profile_path"]
            celeb["tmdb_photo_url"] = f"https://image.tmdb.org/t/p/w300{path}"
            celeb["tmdb_id"] = results[0]["id"]
        else:
            celeb["tmdb_photo_url"] = None

    except Exception as e:
        print(f"  Failed {name}: {e}")
        celeb["tmdb_photo_url"] = None
        time.sleep(2)
        continue

    if (i + 1) % 50 == 0:
        with open(META_PATH, "w") as f:
            json.dump(metadata, f, indent=2)
        print(f"  [{i+1}/{len(metadata)}] saved...", flush=True)

    time.sleep(0.25)

with open(META_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print("Done. TMDB URLs added to metadata.")
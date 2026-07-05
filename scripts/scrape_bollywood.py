import os
import time
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
SAVE_DIR = "data/celebs"

# session with automatic retry
session = requests.Session()
retry = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)

def download_image(url, save_path):
    try:
        response = session.get(url, timeout=15)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"    Failed: {e}")
    return False

def scrape_bollywood():
    print("Searching TMDB for Indian/Bollywood celebrities...")

    dynamic_ids = []
    for page in range(1, 11):  # 10 pages = ~200 people
        try:
            url = "https://api.themoviedb.org/3/person/popular"
            res = session.get(url, params={
                "api_key": API_KEY,
                "page": page,
                "region": "IN"
            }, timeout=15)

            if res.status_code != 200:
                print(f"  Page {page} error: {res.status_code}")
                continue

            for person in res.json().get("results", []):
                name = person["name"].replace(" ", "_").replace("/", "_")
                dynamic_ids.append((person["id"], name, person.get("gender", 0)))

            print(f"  Page {page} done — {len(dynamic_ids)} celebs so far")
            time.sleep(0.5)

        except Exception as e:
            print(f"  Page {page} failed: {e}, skipping...")
            time.sleep(2)
            continue

    print(f"\nFound {len(dynamic_ids)} Bollywood celebrities. Downloading photos...")
    downloaded_total = 0

    for person_id, name, gender in dynamic_ids:
        celeb_dir = os.path.join(SAVE_DIR, name)

        if os.path.exists(celeb_dir) and len(os.listdir(celeb_dir)) >= 3:
            continue

        os.makedirs(celeb_dir, exist_ok=True)

        try:
            img_url = f"https://api.themoviedb.org/3/person/{person_id}/images"
            img_res = session.get(img_url, params={"api_key": API_KEY}, timeout=15)
            profiles = img_res.json().get("profiles", [])[:5]
        except Exception as e:
            print(f"  Skipping {name}: {e}")
            time.sleep(1)
            continue

        if not profiles:
            continue

        downloaded = 0
        for i, profile in enumerate(profiles):
            img_path = f"https://image.tmdb.org/t/p/h632{profile['file_path']}"
            save_path = os.path.join(celeb_dir, f"{i}.jpg")
            if download_image(img_path, save_path):
                downloaded += 1

        downloaded_total += downloaded
        print(f"  {name}: {downloaded} photos")
        time.sleep(0.3)

    print(f"\nDone. {downloaded_total} Bollywood photos downloaded.")

if __name__ == "__main__":
    scrape_bollywood()
import os
import time
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
SAVE_DIR = "data/celebs"
TOTAL_PAGES = 50

os.makedirs(SAVE_DIR, exist_ok=True)

def make_session():
    """Create a fresh session. Called on startup and after fatal connection resets."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    return session

session = make_session()
def robust_get(url, params=None, timeout=20, max_attempts=4):
    global session
    for attempt in range(1, max_attempts + 1):
        try:
            resp = session.get(url, params=params, timeout=timeout)
            return resp
        except requests.exceptions.ConnectionError as e:
            err_str = str(e)
            wait = 5 * attempt  # 5, 10, 15 seconds — longer than before
            print(f"    Connection error (attempt {attempt}/{max_attempts}), waiting {wait}s: {e}")
            if "10054" in err_str or "Connection aborted" in err_str:
                session = make_session()  # stale keep-alive; get fresh session
            time.sleep(wait)
        except requests.exceptions.Timeout as e:
            wait = 3 * attempt
            print(f"    Timeout (attempt {attempt}/{max_attempts}), waiting {wait}s")
            time.sleep(wait)
        except Exception as e:
            print(f"    Unexpected error, skipping: {e}")
            break
    return None


def download_image(url, save_path):
    resp = robust_get(url, timeout=20)
    if resp is not None and resp.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(resp.content)
        return True
    return False


def scrape_celebs():
    total_downloaded = 0
    total_skipped = 0

    for page in range(1, TOTAL_PAGES + 1):
        print(f"\nPage {page}/{TOTAL_PAGES}...")

        res = robust_get(
            "https://api.themoviedb.org/3/person/popular",
            params={"api_key": API_KEY, "page": page},
        )

        if res is None:
            print(f"  Page {page}: all retries failed, skipping.")
            continue
        if res.status_code != 200:
            print(f"  API error {res.status_code}, skipping page.")
            time.sleep(2)
            continue

        people = res.json().get("results", [])

        for person in people:
            name = person["name"].replace(" ", "_").replace("/", "_")
            person_id = person["id"]
            celeb_dir = os.path.join(SAVE_DIR, name)

            if os.path.exists(celeb_dir) and len(os.listdir(celeb_dir)) >= 3:
                total_skipped += 1
                continue

            os.makedirs(celeb_dir, exist_ok=True)

            img_res = robust_get(
                f"https://api.themoviedb.org/3/person/{person_id}/images",
                params={"api_key": API_KEY},
            )

            if img_res is None or img_res.status_code != 200:
                print(f"  Skipping {name}: couldn't fetch image list.")
                continue

            profiles = img_res.json().get("profiles", [])[:5]
            if not profiles:
                continue

            downloaded = 0
            for i, profile in enumerate(profiles):
                img_url = f"https://image.tmdb.org/t/p/h632{profile['file_path']}"
                save_path = os.path.join(celeb_dir, f"{i}.jpg")
                if download_image(img_url, save_path):
                    downloaded += 1
                time.sleep(0.1)   # small gap between image downloads

            total_downloaded += downloaded
            print(f"  {name}: {downloaded} photos")

        time.sleep(1.5)   # be polite between pages

    print(f"\nDone. {total_downloaded} photos downloaded, {total_skipped} skipped.")


if __name__ == "__main__":
    scrape_celebs()
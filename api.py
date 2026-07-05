import os
import uuid
import json
import shutil
import numpy as np
import faiss
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from deepface import DeepFace
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

INDEX_PATH = "models/index.faiss"
META_PATH = "models/meta.json"
CELEBS_DIR = "data/celebs"

# load index and metadata on startup
print("Loading index...", flush=True)

if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r") as f:
        metadata = json.load(f)
    print(f"Loaded {len(metadata)} celebrities.", flush=True)
else:
    index = None
    metadata = []
    print("WARNING: No index found. Run build_index.py first.", flush=True)


def get_embedding(img_path: str):
    result = DeepFace.represent(
        img_path=img_path,
        model_name="ArcFace",
        detector_backend="retinaface",
        enforce_detection=True,
    )
    vec = np.array(result[0]["embedding"], dtype="float32")
    vec /= np.linalg.norm(vec)
    return vec


@app.get("/")
def health():
    return {
        "status": "ok",
        "celebrities_indexed": len(metadata)
    }


@app.post("/match")
async def match_face(
    file: UploadFile = File(...),
    gender: str = Form("any"),
    industry: str = Form("both")
):
    if index is None or len(metadata) == 0:
        return {"error": "Index not built yet. Run build_index.py first."}

    tmp_path = f"data/test_faces/tmp_{uuid.uuid4()}.jpg"
    os.makedirs("data/test_faces", exist_ok=True)

    try:
        with open(tmp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        query_vec = get_embedding(tmp_path)

        # search more candidates so we can filter
        scores, indices = index.search(query_vec.reshape(1, -1), 50)

        matches = []
        for score, idx in zip(scores[0], indices[0]):
            celeb = metadata[idx]

            # gender filter
            if gender != "any":
                if celeb.get("gender", "unknown") != gender:
                    continue

            # industry filter
            celeb_name = celeb.get("name", "").lower()
            celeb_folder = celeb.get("folder", "")
            is_bollywood = celeb.get("industry") == "bollywood"

            if industry == "bollywood" and not is_bollywood:
                continue
            if industry == "hollywood" and is_bollywood:
                continue

            # use TMDB CDN url instead of local file
            photo_url = celeb.get("tmdb_photo_url") or None
            matches.append({
                "celebrity": celeb["name"],
                "score": round(float(score) * 100, 1),
                "photo_url": photo_url
            })

            if len(matches) == 5:
                break

        if not matches:
            return {"error": "No matches found for selected filters. Try different filters."}

        return {"matches": matches}

    except Exception as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
@app.get("/landing-celebs")
def landing_celebs():
    featured = [
        "Brad Pitt", "Scarlett Johansson", "Anne Hathaway",
        "Tom Cruise", "Angelina Jolie", "Jennifer Aniston",
        "Tom Hanks", "Anya Taylor-Joy", "Jennifer Lawrence",
        "Bradley Cooper", "Shah Rukh Khan", "Akshay Kumar"
    ]

    result = []
    for name in featured:
        match = next((m for m in metadata if m["name"] == name), None)
        if match and match.get("tmdb_photo_url"):
            result.append({
                "name": name,
                "photo_url": match["tmdb_photo_url"]
            })

    return {"celebs": result}


# serve celebrity photos as static files
if os.path.exists(CELEBS_DIR):
    app.mount("/celeb-photos", StaticFiles(directory=CELEBS_DIR), name="celeb-photos")


import json
import os
from deepface import DeepFace

META_PATH = "models/meta.json"
CELEBS_DIR = "data/celebs"

with open(META_PATH, "r") as f:
    metadata = json.load(f)

print(f"Analyzing gender for {len(metadata)} celebrities locally...")

for i, celeb in enumerate(metadata):
    if "gender" in celeb:
        continue

    folder = celeb.get("folder", celeb["name"].replace(" ", "_"))
    celeb_dir = os.path.join(CELEBS_DIR, folder)

    if not os.path.exists(celeb_dir):
        celeb["gender"] = "unknown"
        continue

    photos = [f for f in os.listdir(celeb_dir) if f.endswith(".jpg")]
    if not photos:
        celeb["gender"] = "unknown"
        continue

    # try first photo
    photo_path = os.path.join(celeb_dir, photos[0])
    try:
        result = DeepFace.analyze(
            img_path=photo_path,
            actions=["gender"],
            detector_backend="opencv",
            enforce_detection=False,
            silent=True
        )
        gender_scores = result[0]["gender"]
        # pick whichever gender scored higher
        celeb["gender"] = "male" if gender_scores["Man"] > gender_scores["Woman"] else "female"
    except Exception:
        celeb["gender"] = "unknown"

    if (i + 1) % 50 == 0:
        with open(META_PATH, "w") as f:
            json.dump(metadata, f, indent=2)
        print(f"  [{i+1}/{len(metadata)}] saved", flush=True)

with open(META_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print("Done. Gender tags added locally.")
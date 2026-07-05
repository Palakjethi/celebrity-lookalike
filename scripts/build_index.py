import sys
print("Script started", flush=True)

try:
    import os
    import json
    import time
    import numpy as np
    import faiss
    from deepface import DeepFace
    from deepface.modules import modeling
    print("Imports OK", flush=True)
except Exception as e:
    print(f"Import error: {e}", flush=True)
    sys.exit(1)

CELEBS_DIR = "data/celebs"
INDEX_PATH = "models/index.faiss"
META_PATH = "models/meta.json"
PROGRESS_PATH = "models/progress.json"
DETECTOR = "retinaface"   # switched from opencv

os.makedirs("models", exist_ok=True)

print("Loading ArcFace model into memory...", flush=True)
model = modeling.build_model(task="facial_recognition", model_name="ArcFace")
print("Model loaded.", flush=True)

if os.path.exists(PROGRESS_PATH):
    with open(PROGRESS_PATH, "r") as f:
        progress = json.load(f)
    embeddings = [np.array(e, dtype="float32") for e in progress["embeddings"]]
    metadata = progress["metadata"]
    done_folders = set(m["folder"] for m in metadata)
    print(f"Resuming: {len(done_folders)} celebs already done.", flush=True)
else:
    embeddings = []
    metadata = []
    done_folders = set()

celebs = sorted(os.listdir(CELEBS_DIR))
total = len(celebs)
print(f"Found {total} celebrities total. {len(done_folders)} already processed.", flush=True)

skipped = 0
processed = len(done_folders)

def save_progress():
    with open(PROGRESS_PATH, "w") as f:
        json.dump({
            "embeddings": [e.tolist() for e in embeddings],
            "metadata": metadata
        }, f)

start_time = time.time()

for i, celeb_name in enumerate(celebs):
    if celeb_name in done_folders:
        continue

    celeb_dir = os.path.join(CELEBS_DIR, celeb_name)
    if not os.path.isdir(celeb_dir):
        continue

    photos = [f for f in os.listdir(celeb_dir) if f.endswith(".jpg")]
    celeb_embeddings = []

    for photo in photos:
        photo_path = os.path.join(celeb_dir, photo)
        try:
            result = DeepFace.represent(
                img_path=photo_path,
                model_name="ArcFace",
                detector_backend=DETECTOR,
                enforce_detection=True,
            )
            vec = np.array(result[0]["embedding"], dtype="float32")
            celeb_embeddings.append(vec)
        except Exception:
            skipped += 1
            continue

    if not celeb_embeddings:
        continue

    avg_vec = np.mean(celeb_embeddings, axis=0)
    avg_vec /= np.linalg.norm(avg_vec)

    embeddings.append(avg_vec)
    metadata.append({"name": celeb_name.replace("_", " "), "folder": celeb_name})
    processed += 1

    if processed % 10 == 0:
        save_progress()
        elapsed = time.time() - start_time
        rate = (processed - len(done_folders)) / elapsed if elapsed > 0 else 0
        remaining = (total - processed) / rate if rate > 0 else 0
        print(f"  [{processed}/{total}] checkpoint saved, {skipped} skipped, "
              f"{rate:.3f} celebs/sec, ~{remaining/60:.1f} min remaining", flush=True)

save_progress()
print(f"\nBuilding FAISS index with {processed} celebrities...", flush=True)

vecs = np.stack(embeddings).astype("float32")
dim = vecs.shape[1]

index = faiss.IndexFlatIP(dim)
index.add(vecs)

faiss.write_index(index, INDEX_PATH)
with open(META_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"Done. {processed} celebrities indexed, {skipped} photos skipped.", flush=True)
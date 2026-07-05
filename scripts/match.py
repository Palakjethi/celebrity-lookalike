import sys
import json
import numpy as np
import faiss
import cv2
from deepface import DeepFace

INDEX_PATH = "models/index.faiss"
META_PATH = "models/meta.json"
CAPTURED_PATH = "data/test_faces/captured.jpg"

print("Loading index...", flush=True)
index = faiss.read_index(INDEX_PATH)
with open(META_PATH, "r") as f:
    metadata = json.load(f)
print(f"Loaded {len(metadata)} celebrities.", flush=True)

def capture_from_webcam():
    """Opens webcam, lets you press SPACE to capture, ESC to cancel."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam.", flush=True)
        sys.exit(1)

    print("\nWebcam open. Press SPACE to capture, ESC to cancel.", flush=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame.", flush=True)
            break

        cv2.imshow("Press SPACE to capture - ESC to cancel", frame)
        key = cv2.waitKey(1)

        if key % 256 == 27:  # ESC
            print("Cancelled.", flush=True)
            cap.release()
            cv2.destroyAllWindows()
            sys.exit(0)
        elif key % 256 == 32:  # SPACE
            cv2.imwrite(CAPTURED_PATH, frame)
            print(f"Photo captured -> {CAPTURED_PATH}", flush=True)
            break

    cap.release()
    cv2.destroyAllWindows()
    return CAPTURED_PATH

def find_lookalike(img_path, top_k=5):
    result = DeepFace.represent(
        img_path=img_path,
        model_name="ArcFace",
        detector_backend="retinaface",
        enforce_detection=True
    )
    query_vec = np.array(result[0]["embedding"], dtype="float32")
    query_vec /= np.linalg.norm(query_vec)

    scores, indices = index.search(query_vec.reshape(1, -1), top_k)

    matches = []
    for score, idx in zip(scores[0], indices[0]):
        matches.append({
            "celebrity": metadata[idx]["name"],
            "score": round(float(score) * 100, 1)
        })
    return matches

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # use a provided image path
        img_path = sys.argv[1]
    else:
        # no path given -> open webcam
        img_path = capture_from_webcam()

    print(f"\nFinding lookalike for: {img_path}\n", flush=True)

    try:
        results = find_lookalike(img_path)
        print("Top matches:")
        for r in results:
            print(f"  {r['celebrity']}: {r['score']}%")
    except Exception as e:
        print(f"No face detected or error: {e}", flush=True)
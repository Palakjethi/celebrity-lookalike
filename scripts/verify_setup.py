import sys
print(f"Python: {sys.version}")

print("Testing numpy...")
import numpy as np
print(f"  numpy {np.__version__} OK")

print("Testing DeepFace...")
from deepface import DeepFace
print("  DeepFace imported OK")

print("Testing FAISS...")
import faiss
d = 512
index = faiss.IndexFlatIP(d)
dummy = np.random.rand(1, d).astype("float32")
index.add(dummy)
score, idx = index.search(dummy, 1)
assert idx[0][0] == 0
print("  FAISS OK")

print("Testing FastAPI...")
import fastapi
print(f"  FastAPI {fastapi.__version__} OK")

print("\nAll checks passed. Ready to build.")
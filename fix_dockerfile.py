import os
from huggingface_hub import HfApi

# Set this in your shell first:
#   Windows (PowerShell):  $env:HF_TOKEN="your_new_token_here"
#   Then run this script.
token = os.environ.get("HF_TOKEN")
if not token:
    raise SystemExit("Set HF_TOKEN environment variable first.")

api = HfApi(token=token)

dockerfile = """FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libgl1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data/test_faces

EXPOSE 7860

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
"""

with open("hf-space/Dockerfile", "w") as f:
    f.write(dockerfile)

api.upload_file(
    path_or_fileobj="hf-space/Dockerfile",
    path_in_repo="Dockerfile",
    repo_id="PalakJethi/celebrity-lookalike",
    repo_type="space"
)

print("Dockerfile updated!")
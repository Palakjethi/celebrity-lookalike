from huggingface_hub import HfApi

api = HfApi(token="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")

repo_id = "PalakJethi/celebrity-lookalike"
repo_type = "space"

# Upload files
api.upload_file(path_or_fileobj="api.py", path_in_repo="api.py", repo_id=repo_id, repo_type=repo_type)
api.upload_file(path_or_fileobj="requirements.txt", path_in_repo="requirements.txt", repo_id=repo_id, repo_type=repo_type)
api.upload_file(path_or_fileobj="models/index.faiss", path_in_repo="models/index.faiss", repo_id=repo_id, repo_type=repo_type)
api.upload_file(path_or_fileobj="models/meta.json", path_in_repo="models/meta.json", repo_id=repo_id, repo_type=repo_type)
api.upload_file(path_or_fileobj="hf-space/Dockerfile", path_in_repo="Dockerfile", repo_id=repo_id, repo_type=repo_type)

print("All files uploaded successfully!")
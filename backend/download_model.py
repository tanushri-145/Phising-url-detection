from pathlib import Path
from huggingface_hub import hf_hub_download

model_dir = Path(__file__).parent / "models"
model_dir.mkdir(exist_ok=True)

model_path = hf_hub_download(
    repo_id="pirocheto/phishing-url-detection",
    filename="model.onnx",
    local_dir=str(model_dir)
)

print("Model downloaded successfully!")
print("Saved at:", model_path)
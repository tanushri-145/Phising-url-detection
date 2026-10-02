from pathlib import Path

import numpy as np
import onnxruntime as ort
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Locate the downloaded model
MODEL_PATH = Path(__file__).parent / "models" / "model.onnx"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

# Load the model
session = ort.InferenceSession(
    str(MODEL_PATH),
    providers=["CPUExecutionProvider"]
)

print("Phishing detection model loaded!")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "")

    if not isinstance(url, str) or not url.strip():
        return jsonify({"error": "Please enter a URL"}), 400

    url = url.strip()

    try:
        inputs = np.array([url], dtype=str)

        results = session.run(None, {"inputs": inputs})
        probabilities = results[1]

        phishing_probability = float(probabilities[0][1])

        prediction = (
            "Phishing"
            if phishing_probability >= 0.5
            else "Likely legitimate"
        )

        return jsonify({
            "url": url,
            "prediction": prediction,
            "phishing_probability": round(
                phishing_probability * 100, 2
            )
        })

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "Unable to analyze this URL"
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
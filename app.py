from pathlib import Path
import uuid
from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from anpr.detector import ANPRPipeline

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

ALLOWED = {"jpg", "jpeg", "png"}
app = Flask(__name__)
pipeline = ANPRPipeline()

def allowed(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in ALLOWED

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify(pipeline.health())

@app.post("/api/detect")
def detect():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    f = request.files["file"]
    if not f.filename or not allowed(f.filename):
        return jsonify({"error": "Upload a JPG, JPEG or PNG image"}), 400

    name = f"{uuid.uuid4().hex}_{secure_filename(f.filename)}"
    path = UPLOAD_DIR / name
    f.save(path)

    try:
        return jsonify(pipeline.process(str(path), str(OUTPUT_DIR)))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

@app.get("/outputs/<path:name>")
def output(name):
    return send_from_directory(OUTPUT_DIR, name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

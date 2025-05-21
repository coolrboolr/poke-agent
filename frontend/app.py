from pathlib import Path
from flask import Flask, send_from_directory, jsonify
import json

app = Flask(__name__, static_folder="static")
LOG_DIR = Path("logs")
DIAG_DIR = LOG_DIR / "diagnostics"

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/frame.jpg")
def frame_jpg():
    path = LOG_DIR / "frame.jpg"
    if path.exists():
        return send_from_directory(LOG_DIR, "frame.jpg")
    return ("", 404)

@app.route("/diagnostics/<path:name>")
def diagnostics(name):
    file_path = DIAG_DIR / name
    if file_path.exists():
        return send_from_directory(DIAG_DIR, name)
    return jsonify({})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

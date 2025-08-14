from flask import Flask, request, send_file, jsonify
import subprocess, os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

@app.route("/exercises", methods=["GET"])
def list_exercises():
    import json
    with open(os.path.join(BASE_DIR, "exercises.json")) as f:
        exercises = json.load(f)
    return jsonify([e["name"] for e in exercises])

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    exercise = data.get("exercise")
    output_file = os.path.join(OUTPUT_DIR, f"{exercise}_final.mov")
    if not os.path.exists(output_file):
        # Call Blender in background mode
        subprocess.run([
            "blender", "-b", "-P", os.path.join(BASE_DIR, "generate_animation.py"), "--", exercise
        ])
    return send_file(output_file, mimetype='video/quicktime')

if __name__ == "__main__":
    app.run(debug=True)

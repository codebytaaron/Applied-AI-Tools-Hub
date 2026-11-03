link-tracker/
├── app.py
├── data.json
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"links": {}}, f)

def read_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/click/<link_id>")
def click(link_id):
    data = read_data()
    data["links"][link_id] = data["links"].get(link_id, 0) + 1
    write_data(data)
    return jsonify(success=True)

@app.route("/stats")
def stats():
    return jsonify(read_data())

if __name__ == "__main__":
    app.run(debug=True)

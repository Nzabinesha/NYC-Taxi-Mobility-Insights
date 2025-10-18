from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from db import fetchall
import os

# Frontend folder path
FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), "../frontend")

app = Flask(__name__, static_folder=FRONTEND_FOLDER)
CORS(app)

# -----------------------
# 1️⃣ Custom Algorithm (No Built-in Sort)
# -----------------------
def top_k_trips(trips, k=10, sort_by='trip_distance_km'):
    top_trips = []
    for trip in trips:
        inserted = False
        for i in range(len(top_trips)):
            if trip[sort_by] > top_trips[i][sort_by]:
                top_trips.insert(i, trip)
                inserted = True
                break
        if not inserted and len(top_trips) < k:
            top_trips.append(trip)
        if len(top_trips) > k:
            top_trips.pop()
    return top_trips

# -----------------------
# 2️⃣ API ROUTES
# -----------------------

# Basic: Fetch 100 trips
@app.route("/trips")
def get_trips():
    return jsonify(fetchall("SELECT * FROM trips LIMIT 100"))

# Algorithm-based endpoint
@app.route("/top_trips")
def get_top_trips():
    sort_by = request.args.get('sort_by', 'trip_distance_km')
    trips = fetchall("SELECT * FROM trips LIMIT 1000")  # Pull more for ranking
    ranked = top_k_trips(trips, k=10, sort_by=sort_by)
    return jsonify(ranked)

# -----------------------
# 3️⃣ Serve Frontend
# -----------------------
@app.route("/")
def index():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_FOLDER, path)

# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



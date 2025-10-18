from flask import Flask, jsonify, request
from db import fetchall

app = Flask(__name__)

# 1️⃣ Custom Algorithm
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

# 2️⃣ API Endpoint
@app.route('/top_trips', methods=['GET'])
def get_top_trips():
    sort_by = request.args.get('sort_by', 'trip_distance_km')
    trips = fetchall("SELECT * FROM trips LIMIT 1000")  # or fewer rows for testing
    ranked = top_k_trips(trips, k=10, sort_by=sort_by)
    return jsonify(ranked)

if __name__ == '__main__':
    app.run(debug=True)

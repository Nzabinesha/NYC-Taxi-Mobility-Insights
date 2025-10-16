# server.py
from flask import Flask, jsonify, request, render_template
import mysql.connector
from mysql.connector import Error
from pathlib import Path

app = Flask(__name__)

# -------------------------
# Database Configuration
# -------------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shakiratullah@1234',  # Update your MySQL password
    'database': 'nyc_taxi_db'
}

# -------------------------
# Database Utility
# -------------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# -------------------------
# HTML Templates Route
# -------------------------
@app.route('/')
def index():
    """Home page showing simple info"""
    return render_template('index.html')  # Make sure templates/index.html exists

@app.route('/trips_html')
def trips_html():
    """Render all trips in an HTML table"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trips LIMIT 100")  # limit to 100 for HTML view
    trips = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('trips.html', trips=trips)

# -------------------------
# JSON API Endpoints
# -------------------------
@app.route('/api/trips', methods=['GET'])
def get_trips():
    """Return trips as JSON, with optional filters"""
    vendor_id = request.args.get('vendor_id')
    min_distance = request.args.get('min_distance', type=float)
    max_distance = request.args.get('max_distance', type=float)

    query = "SELECT * FROM trips WHERE 1=1"
    params = []

    if vendor_id:
        query += " AND vendor_id = %s"
        params.append(vendor_id)
    if min_distance:
        query += " AND trip_distance_km >= %s"
        params.append(min_distance)
    if max_distance:
        query += " AND trip_distance_km <= %s"
        params.append(max_distance)

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(rows)

@app.route('/api/trips/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    """Get a single trip by trip_id"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trips WHERE trip_id = %s", (trip_id,))
    trip = cursor.fetchone()
    cursor.close()
    conn.close()

    if not trip:
        return jsonify({'error': 'Trip not found'}), 404

    return jsonify(trip)

@app.route('/api/vendors', methods=['GET'])
def get_vendors():
    """Return all vendors"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vendors")
    vendors = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(vendors)

@app.route('/api/analytics', methods=['GET'])
def analytics():
    """Basic aggregated stats"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            COUNT(*) AS total_trips,
            AVG(trip_distance_km) AS avg_distance_km,
            AVG(speed_kmph) AS avg_speed_kmph
        FROM trips
    """)
    stats = cursor.fetchone()
    cursor.close()
    conn.close()

    return jsonify(stats)

# -------------------------
# Run Server
# -------------------------
if __name__ == '__main__':
    # Ensure template folder exists
    template_dir = Path(__file__).parent / 'templates'
    template_dir.mkdir(exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

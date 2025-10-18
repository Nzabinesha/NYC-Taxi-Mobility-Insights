import csv
import mysql.connector

# ------------------------------
# Database connection configuration
# ------------------------------
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123',  # update with your MariaDB password
    'database': 'nyc_taxi_db'
}

# ------------------------------
# CSV file path and batch size
# ------------------------------
csv_file_path = '../data/processed/cleaned_train.csv'
batch_size = 10000  # adjust for faster inserts if memory allows

# ------------------------------
# SQL statements
# ------------------------------
vendor_query = "INSERT IGNORE INTO vendors (vendor_id) VALUES (%s)"
trips_query = """
    INSERT INTO trips (
        trip_id, vendor_id, pickup_datetime, dropoff_datetime,
        passenger_count, store_and_fwd_flag, trip_duration,
        trip_distance_km, speed_kmph, pickup_hour, pickup_dayofweek
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
locations_query = """
    INSERT INTO locations (
        trip_id, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude
    ) VALUES (%s, %s, %s, %s, %s)
"""

# ------------------------------
# Day mapping for pickup_dayofweek
# ------------------------------
day_map = {
    'Sunday': 0,
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6
}

# ------------------------------
# Main insertion logic
# ------------------------------
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        vendor_batch = set()  # to avoid duplicate vendor inserts
        trips_batch = []
        locations_batch = []

        total_rows = 0

        for row in reader:
            total_rows += 1

            # Clean trip_id: remove 'id' prefix and convert to integer
            trip_id = int(row['id'].replace('id', '').strip())

            # Map day name to integer
            pickup_dayofweek = day_map.get(row['pickup_dayofweek'], None)

            # Vendor batch
            vendor_batch.add((row['vendor_id'],))

            # Trips batch
            trips_batch.append((
                trip_id,
                row['vendor_id'],
                row['pickup_datetime'],
                row['dropoff_datetime'],
                row['passenger_count'],
                row['store_and_fwd_flag'],
                row['trip_duration'],
                row['trip_distance_km'],
                row['speed_kmph'],
                row['pickup_hour'],
                pickup_dayofweek
            ))

            # Locations batch
            locations_batch.append((
                trip_id,
                row['pickup_longitude'],
                row['pickup_latitude'],
                row['dropoff_longitude'],
                row['dropoff_latitude']
            ))

            # Execute batch if reached batch_size
            if len(trips_batch) >= batch_size:
                cursor.executemany(vendor_query, list(vendor_batch))
                cursor.executemany(trips_query, trips_batch)
                cursor.executemany(locations_query, locations_batch)
                connection.commit()
                vendor_batch.clear()
                trips_batch.clear()
                locations_batch.clear()
                print(f"Inserted {total_rows} rows so far...")

        # Insert any remaining rows
        if trips_batch:
            cursor.executemany(vendor_query, list(vendor_batch))
            cursor.executemany(trips_query, trips_batch)
            cursor.executemany(locations_query, locations_batch)
            connection.commit()
            print(f"Inserted total of {total_rows} rows.")

    print("CSV data inserted successfully into vendors, trips, and locations!")

finally:
    cursor.close()
    connection.close()


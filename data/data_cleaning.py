"""
NYC Taxi Trip Data Cleaning Script (Simplified Dataset)
------------------------------------------------------
Task 1: Data Processing and Cleaning
Performs:
 - Cleaning missing/invalid data
 - Formatting timestamps
 - Creating derived features
"""

import pandas as pd
import numpy as np

# === FILE PATHS ===
RAW_FILE = "train.csv"
CLEAN_FILE = "cleaned_train.csv"
LOG_FILE = "excluded_records.log"

print("Loading dataset...")
df = pd.read_csv(RAW_FILE)
print(f"Initial shape: {df.shape}")

# === HANDLE DUPLICATES ===
df.drop_duplicates(inplace=True)

# === HANDLE MISSING VALUES ===
df.dropna(subset=[
    'pickup_datetime', 'dropoff_datetime',
    'pickup_longitude', 'pickup_latitude',
    'dropoff_longitude', 'dropoff_latitude'
], inplace=True)

# === CONVERT TIMESTAMPS ===
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'], errors='coerce')
df = df.dropna(subset=['pickup_datetime', 'dropoff_datetime'])

# === DERIVED FEATURES ===
# 1. Trip distance (km)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2)**2
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

df['trip_distance_km'] = haversine(
    df['pickup_latitude'], df['pickup_longitude'],
    df['dropoff_latitude'], df['dropoff_longitude']
)

# 2. Average speed (km/h)
df['speed_kmph'] = df['trip_distance_km'] / (df['trip_duration'] / 3600)

# 3. Pickup hour of day
df['pickup_hour'] = df['pickup_datetime'].dt.hour

# 4. Day of week
df['pickup_dayofweek'] = df['pickup_datetime'].dt.day_name()

# === FILTER OUT INVALID RECORDS ===
invalid_mask = (
    (df['trip_duration'] <= 0) |
    (df['trip_distance_km'] <= 0) |
    (df['speed_kmph'] > 120)
)
excluded = df[invalid_mask]
df_cleaned = df[~invalid_mask]

excluded.to_csv(LOG_FILE, index=False)
print(f"Excluded {len(excluded)} invalid records logged in {LOG_FILE}")

# === SAVE CLEAN DATA ===
df_cleaned.to_csv(CLEAN_FILE, index=False)
print(f"Clean dataset saved to {CLEAN_FILE}")
print(f"Final shape: {df_cleaned.shape}")

print("\nDerived Features:")
print("- trip_distance_km")
print("- speed_kmph")
print("- pickup_hour")
print("- pickup_dayofweek")

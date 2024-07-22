import psycopg2
import random
from datetime import datetime, timedelta
import string

# Database connection details
host = "localhost"
database = "vsignals"
user = "vsignals"
password = "VSignals123"

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

# Create a cursor object
cur = conn.cursor()

# Create a table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS signals (
        id SERIAL PRIMARY KEY,
        vehicle_id VARCHAR(12),
        signal VARCHAR(10),
        speed VARCHAR(10),
        event_timestamp TIMESTAMP
    )
""")

# Number of vehicle IDs and records
NUM_VEHICLE_IDS = 100
NUM_RECORDS = 1_000_000

# Generate vehicle IDs
vehicle_ids = [f'vehicle{i}' for i in range(1, NUM_VEHICLE_IDS + 1)]

# Generate data points
start_time = datetime(2023, 7, 19, 12, 34, 56)

for i in range(NUM_RECORDS):
    vehicle_id = random.choice(vehicle_ids)
    timestamp = start_time + timedelta(seconds=i)
    speed = round(random.uniform(0, 100), 2)

    record = (vehicle_id, 'Speed', str(speed), timestamp)
    if i >= 10_000 and (i % 10_000 == 0 or i == NUM_RECORDS - 1):
        print("insert " + str(i) + " reocrds already")
        conn.commit()
    cur.execute("INSERT INTO signals (vehicle_id, signal, speed, event_timestamp) VALUES (%s, %s, %s, %s)", record)

# Commit the changes and close the connection
cur.close()
conn.close()

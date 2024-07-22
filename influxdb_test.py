from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random
from datetime import datetime, timedelta

# InfluxDB connection details
bucket = "v-signals"
org = "jlr"
token = "ygHbq1VKVxYHReX8ivjDj4ENejJe7edZetdaUkn5KYLQafeyL52Jeju_D3ih__IUd9251SOOdAL12M7DWRQRaw=="
url = "http://localhost:8086"

# Number of vehicle IDs and records
NUM_VEHICLE_IDS = 100
NUM_RECORDS = 1_000_000

# Create a client
client = InfluxDBClient(url=url, token=token, org=org)

# Create a write API instance
write_api = client.write_api(write_options=SYNCHRONOUS)

# Generate vehicle IDs
vehicle_ids = [f'vehicle{i}' for i in range(1, NUM_VEHICLE_IDS + 1)]

# Generate data points
start_time = datetime(2023, 7, 19, 12, 34, 56)

for i in range(NUM_RECORDS):
    vehicle_id = random.choice(vehicle_ids)
    timestamp = start_time + timedelta(seconds=i)
    speed = round(random.uniform(0, 100), 2)

    # Create a data point
    point = Point(vehicle_id).tag("signal", "speed").field("speed", speed)

    # Write the point to InfluxDB
    write_api.write(bucket=bucket, org=org, record=point)

# Close the client
client.close()

import boto3
from boto3.dynamodb.conditions import Key, Attr
import random
from datetime import datetime, timedelta

# Create a DynamoDB client connected to the local endpoint
dynamodb = boto3.client('dynamodb',
    aws_access_key_id="anything",
    aws_secret_access_key="anything",
    region_name="us-west-2",endpoint_url='http://localhost:8000')

# Define the table name
table_name = 'v_signals'

# Create the table if it doesn't exist
try:
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'VehicleID',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'VehicleID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print(f"Table {table_name} created successfully.")
except dynamodb.exceptions.ResourceInUseException:
    print(f"Table {table_name} already exists.")

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

    record = {
        'VehicleID': {'S': vehicle_id + '_' + str(i)},
        'Signal': {'S': 'Speed'},
        'Speed': {'S': str(speed)},
        'EventTimestamp': {'S': str(timestamp)}
    }

    dynamodb.put_item(
        TableName=table_name,
        Item=record
    )

print(f"Wrote record done")

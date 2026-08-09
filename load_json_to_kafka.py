import os
import json
from kafka import KafkaProducer

# Kafka Configuration
BOOTSTRAP_SERVER = "localhost:9092"
TOPIC = "betting-data"

# Producer
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Folders containing JSON files
folders = [
    "OUTPUT_melbet",
    "OUTPUT_1xbet",
    "OUTPUT_10crick",
    "OUTPUT_22xbet",
    "OUTPUT",
    "OUTOUT_1x",
    "OUTPUT_10",
    "OUTPUT22",
    
]

for folder in folders:

    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        continue

    print(f"\nReading files from: {folder}")

    for root, dirs, files in os.walk(folder):

        for file in files:

            if file.endswith(".json"):

                filepath = os.path.join(root, file)

                try:

                    with open(filepath, "r", encoding="utf-8") as f:

                        data = json.load(f)

                    producer.send(TOPIC, value=data)

                    print(f"Published: {filepath}")

                except Exception as e:

                    print(f"Error publishing {filepath}: {e}")

producer.flush()
producer.close()

print("\nAll JSON files have been published to Kafka.")
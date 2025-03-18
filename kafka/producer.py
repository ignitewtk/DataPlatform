from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

events = [
    {"user_id": 1, "action": "click", "item": "shirt"},
    {"user_id": 2, "action": "view", "item": "shoes"},
    {"user_id": 3, "action": "purchase", "item": "hat"}
]

for event in events:
    producer.send('user-events', value=event)
    print(f"Sent: {event}")
    time.sleep(1)

producer.flush()

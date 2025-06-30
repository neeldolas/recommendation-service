from confluent_kafka import Consumer
from app.model import append_rating  # this function appends to your CSV
import json

# Kafka consumer config
consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'recommendation-group',
    'auto.offset.reset': 'earliest'
})

# Subscribe to order-placed topic
consumer.subscribe(['order-events'])

def listen_for_orders():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        # Parse Kafka message value
        order = json.loads(msg.value().decode('utf-8'))

        user_id = order['userId']
        menu_item_id = order['menuItemId']
        rating = order['rating']   # <-- now fetched directly from event
        print(f"✅ Received rating {rating} for user {user_id}, item {menu_item_id}")

        # Append rating to CSV via your model.py function
        append_rating(user_id, menu_item_id, rating)

        print(f"✔️ Updated ratings for user {user_id}, item {menu_item_id}")

if __name__ == "__main__":
    listen_for_orders()

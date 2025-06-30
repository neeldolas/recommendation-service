from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
from app.kafka_consumer import listen_for_orders
from app.recommender import recommend_for_user

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Starting Kafka consumer thread...")
    threading.Thread(target=listen_for_orders, daemon=True).start()
    yield
    print("🛑 Shutting down app...")

# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# REST endpoint to fetch recommendations for a user
@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: int, n: int = 5):
    recommendations = recommend_for_user(user_id, n)
    return {
        "userId": user_id,
        "recommendations": recommendations
    }

@app.get("/ratings")
def get_ratings_csv():
    with open("ratings.csv", "r") as file:
        content = file.read()
    return {"ratings_csv": content}

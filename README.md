# 🍽️ Recommendation Service — DineGrid

A Python FastAPI microservice providing ML-based menu recommendations for users on the DineGrid platform. It consumes order events via Kafka, updates a local ratings dataset, and exposes REST APIs for fetching recommendations.

---

## ⚙️ Tech Stack
- Python 3.11
- FastAPI
- scikit-learn
- Apache Kafka
- Docker

---

## 📊 Features
- Kafka consumer listens to `order-events`
- Updates `ratings.csv` with user-item ratings
- KNN-based recommendation engine using collaborative filtering
- API to fetch top N menu recommendations for a user

---

## 📌 API
- `GET /recommendations/{user_id}` → Fetch recommendations

---

## 🚀 Run with Docker

```bash
docker build -t dinegrid-recommendation-service .
docker run -p 8000:8000 dinegrid-recommendation-service

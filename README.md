

# 🛍️ E-commerce Microservices (FastAPI + Docker)

A simple microservice-based e-commerce application built using **Python (FastAPI)** and **Docker Compose** to demonstrate **inter-service communication via REST APIs**.  
This project is designed as a learning project to understand how microservices interact with each other in a distributed system.

---

## 📜 Project Overview

This mini-project simulates a basic e-commerce flow with **three independent microservices**, each running in its own container and communicating with others via HTTP APIs.

- 🛒 **Product Service** – Manages product catalog (CRUD operations).
- 📦 **Order Service** – Creates and manages orders by calling the Product Service.
- 💳 **Payment Service** – Processes payments by calling the Order Service.

All services are containerized using **Docker Compose** and use **in-memory storage** to keep things simple and focused on microservice communication.

---

## 🧱 Architecture

[Product Service] <---- [Order Service] <---- [Payment Service]
| | |
port:8001 port:8002 port:8003


- **Order Service** calls **Product Service** to validate product details and stock before creating an order.
- **Payment Service** calls **Order Service** to verify total amount before processing payment.

---

## 🐳 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<YOUR_USERNAME>/ecommerce-microservices.git
cd ecommerce-microservices

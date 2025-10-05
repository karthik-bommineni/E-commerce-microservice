from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import httpx

app = FastAPI(title="Order Service", version="1.0.0")

# In-memory order storage
orders: Dict[int, dict] = {}
next_order_id = 1

# Product service URL (we'll call this container by its service name in Docker)
PRODUCT_SERVICE_URL = "http://product-service:8001"

class OrderIn(BaseModel):
    product_id: int
    quantity: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/orders", status_code=201)
async def create_order(order: OrderIn):
    global next_order_id

    # Step 1: Call Product Service API
    async with httpx.AsyncClient() as client:
        product_resp = await client.get(f"{PRODUCT_SERVICE_URL}/products/{order.product_id}")
    
    if product_resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found")

    product = product_resp.json()

    # Step 2: Check stock
    if order.quantity > product["stock"]:
        raise HTTPException(status_code=400, detail="Not enough stock")

    # Step 3: Calculate total price
    total_price = product["price"] * order.quantity

    # Step 4: Save order in memory
    new_order = {
        "id": next_order_id,
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": order.quantity,
        "total_price": total_price,
        "status": "PENDING"
    }

    orders[next_order_id] = new_order
    next_order_id += 1

    return new_order

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

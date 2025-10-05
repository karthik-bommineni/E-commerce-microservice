from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel 
import httpx 
 
app = FastAPI(title="Payment Service", version="1.0.0") 
 
ORDER_SERVICE_URL = "http://order-service:8002" 
 
class PaymentIn(BaseModel): 
    order_id: int 
    amount: float 
 
@app.get("/health") 
def health(): 
    return {"status": "ok"} 
 
@app.post("/payments") 
async def make_payment(payment: PaymentIn): 
    async with httpx.AsyncClient() as client: 
        order_resp = await client.get(f"{ORDER_SERVICE_URL}/orders/{payment.order_id}") 
    if order_resp.status_code != 200: 
        raise HTTPException(status_code=404, detail="Order not found") 
    order = order_resp.json() 
    if payment.amount != order["total_price"]: 
        raise HTTPException(status_code=400, detail="Payment amount does not match order total") 
    order["status"] = "PAID" 
    return {"message": "Payment successful", "order": order}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List

app = FastAPI(title="Product Service", version="1.0.0")

# ----- In-memory store -----
class ProductIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0)
    stock: int = Field(..., ge=0)

class ProductOut(ProductIn):
    id: int

products: Dict[int, ProductOut] = {}
next_id = 1

# ----- Health check -----
@app.get("/health")
def health():
    return {"status": "ok"}

# ----- CRUD-ish -----
@app.get("/products", response_model=List[ProductOut])
def list_products():
    return list(products.values())

@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int):
    product = products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=ProductOut, status_code=201)
def create_product(p: ProductIn):
    global next_id
    new_product = ProductOut(id=next_id, **p.dict())
    products[next_id] = new_product
    next_id += 1
    return new_product

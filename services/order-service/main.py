from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Order Service")

class OrderCreate(BaseModel):
    status: str

@app.get("/orders")
def get_orders():
    return [
        {"id": 1, "status": "Delivered"}
    ]

@app.post("/orders")
def create_order(order: OrderCreate):
    return {"id": 2, "status": order.status}

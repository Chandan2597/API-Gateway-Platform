from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Product Service")

class ProductCreate(BaseModel):
    name: str

@app.get("/products")
def get_products():
    return [
        {"id": 1, "name": "Laptop"}
    ]

@app.post("/products")
def create_product(product: ProductCreate):
    return {"id": 2, "name": product.name}

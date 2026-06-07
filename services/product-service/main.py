from fastapi import FastAPI

app = FastAPI(title="Product Service")

@app.get("/products")
def get_products():
    return [
        {"id": 1, "name": "Laptop"}
    ]

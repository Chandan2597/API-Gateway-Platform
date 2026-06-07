from fastapi import FastAPI

app = FastAPI(title="Order Service")

@app.get("/orders")
def get_orders():
    return [
        {"id": 1, "status": "Delivered"}
    ]

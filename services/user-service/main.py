from fastapi import FastAPI

app = FastAPI(title="User Service")

@app.get("/users")
def get_users():
    return [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Mike"}
    ]

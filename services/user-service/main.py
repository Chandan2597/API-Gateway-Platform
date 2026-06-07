from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="User Service")

class UserCreate(BaseModel):
    name: str

@app.get("/users")
def get_users():
    return [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Mike"}
    ]

@app.post("/users")
def create_user(user: UserCreate):
    return {"id": 3, "name": user.name}

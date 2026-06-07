from fastapi import HTTPException

def check_permissions(user_payload: dict, method: str, path: str):
    if not user_payload:
        if method != "GET":
            raise HTTPException(status_code=401, detail="Authentication required for this action")
        return
    
    role = user_payload.get("role", "user")
    
    if role == "admin":
        return
        
    if role == "user" and method != "GET":
        raise HTTPException(status_code=403, detail="Not enough permissions")

import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr

app = FastAPI()

class User(BaseModel):
    name: str
    email: str

# In-memory storage for users
users_db = {}

@app.post("/create-user", status_code=201)
def create_user(user: User):
    # Basic validation
    if not user.name or not user.email:
        raise HTTPException(status_code=400, detail="Name and email are required.")
    
    if not isinstance(user.name, str) or not isinstance(user.email, str):
        raise HTTPException(status_code=400, detail="Name and Email must be strings.")
        
    if "@" not in user.email or "." not in user.email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Invalid email format.")
        
    if len(user.name) > 255:
        raise HTTPException(status_code=400, detail="Name is too long.")
        
    if len(user.email) > 254:
        raise HTTPException(status_code=400, detail="Email is too long.")

    # Check for duplicates
    for u in users_db.values():
        if u["email"] == user.email:
            raise HTTPException(status_code=409, detail="Email already exists.")
            
    # Success
    user_id = str(uuid.uuid4())
    new_user = {"id": user_id, "name": user.name, "email": user.email}
    users_db[user_id] = new_user
    
    return new_user

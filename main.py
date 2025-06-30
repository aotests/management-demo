from fastapi import FastAPI, HTTPException, status, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import bcrypt
import json
import os
from typing import List, Literal

app = FastAPI()

# API Key Authentication
API_KEY = os.environ.get("API_KEY")

async def get_api_key(x_api_key: str = Header(None)):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

# CORS Middleware Configuration
origins = ["*"]  # Allow all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Models
class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    access_level: Literal["read", "write"]
    is_active: bool = True

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    access_level: Literal["read", "write"]
    is_active: bool

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UpdateAccessLevelRequest(BaseModel):
    access_level: Literal["read", "write"]

# Database file
DB_FILE = "users.json"

# Helper functions
def read_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user_by_email(email: EmailStr):
    users = read_db()
    for user in users:
        if user["email"] == email:
            return user
    return None

# Endpoints
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: User, api_key: str = Depends(get_api_key)):
    """
    Creates a new user.
    """
    if get_user_by_email(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado")
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    user_data = user.dict()
    user_data["password"] = hashed_password.decode('utf-8')
    
    users = read_db()
    users.append(user_data)
    write_db(users)
    
    return user

@app.get("/users", response_model=List[UserResponse])
def get_users(api_key: str = Depends(get_api_key)):
    """
    Returns a list of all users.
    """
    users = read_db()
    return users

@app.post("/login")
def login(request: LoginRequest):
    """
    Authenticates a user.
    """
    user = get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credenciais inválidas")

    if not user["is_active"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")

    if not bcrypt.checkpw(request.password.encode('utf-8'), user["password"].encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    return {
        "name": user["name"],
        "email": user["email"],
        "access_level": user["access_level"]
    }

@app.post("/users/{email}/reset-password", response_model=UserResponse)
def reset_password(email: EmailStr, api_key: str = Depends(get_api_key)):
    """
    Resets a user's password to "teste123".
    """
    users = read_db()
    user_found = False
    for u in users:
        if u["email"] == email:
            user_found = True
            hashed_password = bcrypt.hashpw("teste123".encode('utf-8'), bcrypt.gensalt())
            u["password"] = hashed_password.decode('utf-8')
            write_db(users)
            return u
    
    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

@app.delete("/users/{email}", response_model=UserResponse)
def deactivate_user(email: EmailStr, api_key: str = Depends(get_api_key)):
    """
    Deactivates a user.
    """
    users = read_db()
    user_found = False
    for u in users:
        if u["email"] == email:
            user_found = True
            u["is_active"] = False
            write_db(users)
            return u

    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

@app.post("/users/{email}/reactivate", response_model=UserResponse)
def reactivate_user(email: EmailStr, api_key: str = Depends(get_api_key)):
    """
    Reactivates a user.
    """
    users = read_db()
    user_found = False
    for u in users:
        if u["email"] == email:
            user_found = True
            u["is_active"] = True
            write_db(users)
            return u

    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

@app.put("/users/{email}/access-level", response_model=UserResponse)
def update_access_level(email: EmailStr, request: UpdateAccessLevelRequest, api_key: str = Depends(get_api_key)):
    """
    Updates a user's access level.
    """
    users = read_db()
    user_found = False
    for u in users:
        if u["email"] == email:
            user_found = True
            u["access_level"] = request.access_level
            write_db(users)
            return u

    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

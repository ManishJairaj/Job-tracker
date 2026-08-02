from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name : str 
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)

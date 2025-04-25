from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class Usuario(BaseModel):
    id: Optional[int]
    username: str = Field(default="username", min_length=5,max_length=20)
    activo: bool = Field(default=False)
    password: str = Field(default="password", min_length=5,max_length=50)
    fono: str
    email: EmailStr = Field (default="email", min_length=5,max_length=50)



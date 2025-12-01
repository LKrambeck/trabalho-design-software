from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UsuarioRequest(BaseModel):
    nome: str
    email: str
    telefone: str
    role: RoleEnum

    class Config:
        use_enum_values = True


class UsuarioDBSchema(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    role: RoleEnum

    class Config:
        use_enum_values = True

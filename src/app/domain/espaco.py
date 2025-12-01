from pydantic import BaseModel

class EspacoRequest(BaseModel):
    nome: str
    capacidade: int
    preco: float
    fotos: list[str]


class EspacoDBSchema(BaseModel):
    id: int
    nome: str
    capacidade: int
    preco: float
    fotos: list[str]

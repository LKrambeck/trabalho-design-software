from datetime import date
from pydantic import BaseModel, validator
from typing import Optional

class ReservaRequest(BaseModel):
    espaco_id: int
    usuario_id: int
    data_inicio: date
    data_fim: date

    @property
    def dias_reserva(self) -> int:
        delta = self.data_fim - self.data_inicio
        return delta.days + 1

    @validator("data_inicio")
    def validar_data_inicio(cls, data_inicio):
        if data_inicio <= date.today():
            raise ValueError("data_inicio deve ser uma data futura")
        return data_inicio

    @validator("data_fim")
    def validar_datas(cls, data_fim, values):
        data_inicio = values.get("data_inicio")
        if data_inicio and data_inicio >= data_fim:
            raise ValueError("data_inicio deve ser menor que data_fim")
        return data_fim


class ReservaDBSchema(BaseModel):
    id: int
    espaco_id: int
    usuario_id: int
    data_inicio: date
    data_fim: date
    valor_total: float

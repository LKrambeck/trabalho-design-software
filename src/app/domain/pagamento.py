from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class PagamentoStatusEnum(str, Enum):
    SINAL = "sinal"
    CONCLUIDO = "concluido"


class PagamentoRequest(BaseModel):
    valor_pago: float


class PagamentoDBSchema(BaseModel):
    id: int
    valor_pago: float
    reserva_id: int
    data_pagamento: datetime
    status: PagamentoStatusEnum

    class Config:
        use_enum_values = True

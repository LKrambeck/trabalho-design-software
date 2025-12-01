from app.domain.pagamento import PagamentoRequest, PagamentoDBSchema
from app.repository.pagamento import PagamentoRepository
from app.repository.reserva import ReservaRepository

class NotFoundException(Exception):
    pass

class PagamentoService:
    def read_all() -> list[PagamentoDBSchema]:
        return PagamentoRepository.read_all()

    def read_by_id(pagamento_id: int) -> PagamentoDBSchema | None:
        if pagamento := PagamentoRepository.read_by_id(pagamento_id):
            return pagamento.dict()
        raise NotFoundException()

    def update(pagamento_id: int, updated_pagamento: PagamentoRequest) -> PagamentoDBSchema | None:
        pagamento = PagamentoService.read_by_id(pagamento_id)
        reserva = ReservaRepository.read_by_id(pagamento["reserva_id"])
        if reserva.valor_total != updated_pagamento.valor_pago:
            raise Exception("O valor pago não corresponde ao valor total da reserva.")

        pagamento["valor_pago"] = updated_pagamento.valor_pago
        pagamento["status"] = "concluido"
        pagamento_schema = PagamentoDBSchema(**pagamento)
        if pagamento := PagamentoRepository.update(pagamento_id, pagamento_schema):
            return pagamento.dict()
        raise NotFoundException()

    def delete(pagamento_id: int):
        if not PagamentoRepository.delete(pagamento_id):
            raise NotFoundException()

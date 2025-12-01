from app.domain.reserva import ReservaRequest, ReservaDBSchema
from app.domain.pagamento import PagamentoRequest
from app.repository.reserva import ReservaRepository
from app.repository.pagamento import PagamentoRepository
from app.service.espaco import EspacoService
from app.service.usuario import UsuarioService

class NotFoundException(Exception):
    pass

class ReservaService:
    # implementar semaforo ?? 
    def create(input: ReservaRequest) -> ReservaDBSchema:
        # validar se o espaço está disponivel nas datas solicitadas
        try:
            espaco = EspacoService.read_by_id(input.espaco_id)
        except Exception:
            raise Exception("Espaço não encontrado.")

        try:
            UsuarioService.read_by_id(input.usuario_id)
        except Exception:
            raise Exception("Usuário não encontrado.")

        reservas = ReservaRepository.read_all()
        for reserva in reservas:
            if reserva.espaco_id == input.espaco_id:
                if not (input.data_fim < reserva.data_inicio or input.data_inicio > reserva.data_fim):
                    raise Exception("Espaço indisponível nas datas solicitadas.")

        reserva = input.dict()
        reserva["valor_total"] = espaco["preco"] * input.dias_reserva
        reserva = ReservaRepository.create(reserva)

        pagamento_request = PagamentoRequest(
            valor_pago=reserva.valor_total*0.5,
            reserva_id=reserva.id
        )
        PagamentoRepository.create(pagamento_request)

        return reserva.dict()

    def read_all() -> list[ReservaDBSchema]:
        return ReservaRepository.read_all()

    def read_by_id(reserva_id: int) -> ReservaDBSchema | None:
        if reserva := ReservaRepository.read_by_id(reserva_id):
            return reserva.dict()
        raise NotFoundException()

    def update(reserva_id: int, updated_reserva: ReservaRequest) -> ReservaDBSchema | None:
        reserva_to_update = ReservaRepository.read_by_id(reserva_id)
        if reserva_to_update.espaco_id != updated_reserva.espaco_id:
            raise Exception("Não é permitido alterar o espaço de uma reserva existente")

        if reserva_to_update.usuario_id != updated_reserva.usuario_id:
            raise Exception("Não é permitido alterar o usuário de uma reserva existente")

        reserva = updated_reserva.dict()
        if reserva_to_update.data_inicio != updated_reserva.data_inicio or reserva_to_update.data_fim != updated_reserva.data_fim:
            try:
                espaco = EspacoService.read_by_id(updated_reserva.espaco_id)
            except Exception:
                raise Exception("Espaço não encontrado.")

            reserva["valor_total"] = espaco["preco"] * updated_reserva.dias_reserva

        reserva_schema = ReservaDBSchema(**reserva, id=reserva_id)
        if reserva := ReservaRepository.update(reserva_id, reserva_schema):
            return reserva.dict()
        raise NotFoundException()

    def delete(reserva_id: int):
        if not ReservaRepository.delete(reserva_id):
            raise NotFoundException()

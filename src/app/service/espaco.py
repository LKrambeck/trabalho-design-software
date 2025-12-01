from app.domain.espaco import EspacoRequest
from app.repository.espaco import EspacoRepository, EspacoDBSchema

class NotFoundException(Exception):
    pass


class EspacoService:
    def create(input: EspacoRequest) -> EspacoDBSchema:
        db = EspacoRepository.read_all()
        for espaco in db:
            if espaco.nome == input.nome:
                raise Exception("Espaço já existente.")

        espaco = EspacoRepository.create(input)
        return espaco.dict()

    def read_all() -> list[EspacoDBSchema]:
        return EspacoRepository.read_all()

    def read_by_id(espaco_id: int) -> dict | None:
        if espaco :=  EspacoRepository.read_by_id(espaco_id):
            return espaco.dict()
        raise NotFoundException()

    def update(espaco_id: int, updated_espaco: EspacoRequest) -> EspacoDBSchema | None:
        espaco_schema = EspacoDBSchema(**updated_espaco.dict(), id=espaco_id)
        if espaco := EspacoRepository.update(espaco_id, espaco_schema):
            return espaco.dict()
        raise NotFoundException()

    def delete(espaco_id: int):
        if not EspacoRepository.delete(espaco_id):
            raise NotFoundException()

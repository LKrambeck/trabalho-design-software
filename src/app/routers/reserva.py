from fastapi import APIRouter, Response
from domain.reserva import ReservaRequest, ReservaDBSchema
from service.reserva import ReservaService, NotFoundException

reserva_router = APIRouter(prefix="/reserva", tags=["Reserva"])

@reserva_router.post("/")
def create(input: ReservaRequest, response: Response):
    """
    Cria uma nova reserva.
    """
    try:
        reserva = ReservaService.create(input)
        response.status_code = 201
        return reserva
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

@reserva_router.get("/")
def read(response: Response):
    """
    Retorna todas as reservas cadastradas.
    """
    try:
        reservas = ReservaService.read_all()
        return reservas
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

@reserva_router.get("/{id}")
def read_id(id: str, response: Response):
    """
    Retorna uma reserva específica pelo ID.
    """
    try:
        reserva = ReservaService.read_by_id(int(id))
        return reserva
    except NotFoundException:
        response.status_code = 404
        return {"error": "Reserva não encontrada."}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

@reserva_router.put("/{id}")
def update(id: str, input: ReservaRequest, response: Response):
    """
    Atualiza os dados de uma reserva existente.
    """
    try:
        reserva = ReservaService.update(int(id), input)
        return reserva
    except NotFoundException:
        response.status_code = 404
        return {"error": "Reserva não encontrada."}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

@reserva_router.delete("/{id}")
def delete(id: str, response: Response):
    """
    Remove uma reserva pelo ID.
    """
    try:
        ReservaService.delete(int(id))
        return {"message": "Reserva deletada com sucesso."}
    except NotFoundException:
        response.status_code = 404
        return {"error": "Reserva não encontrada."}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

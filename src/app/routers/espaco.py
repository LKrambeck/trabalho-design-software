from app.domain.espaco import EspacoRequest
from app.domain.espaco import EspacoDBSchema
from app.service.espaco import EspacoService
from app.service.espaco import NotFoundException
from fastapi import APIRouter
from fastapi import Response

espaco_router = APIRouter(prefix="/espaco", tags=["Espaço"])

RESPONSE_CREATE = {
    201: {
        "description": "Espaço criado com sucesso.",
    }
}

@espaco_router.post("/", responses=RESPONSE_CREATE)
def create(input: EspacoRequest, response: Response):
    """
    Cria um novo espaço.
    """
    try:
        espaco = EspacoService.create(input)
        response.status_code = 201
        return espaco
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}


@espaco_router.get("/")
def read(response: Response):
    """
    Retorna todos os espaços cadastrados.
    """
    try:
        espacos = EspacoService.read_all()
        return espacos
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}


@espaco_router.get("/{id}")
def read_id(id: str, response: Response):
    """
    Retorna um espaço específico pelo ID.
    """
    try:
        espaco = EspacoService.read_by_id(int(id))
        return espaco
    except NotFoundException:
        response.status_code = 404
        return {"error": "Espaço não encontrado."}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}


@espaco_router.put("/{id}")
def update(id: str, input: EspacoRequest, response: Response):
    """
    Atualiza os dados de um espaço existente.
    """
    try:
        espaco = EspacoService.update(int(id), input)
        return espaco
    except NotFoundException:
        response.status_code = 404
        return {"error": "Espaço não encontrado."}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}


@espaco_router.delete("/{id}")
def delete(id: str, response: Response):
    """
    Remove um espaço pelo ID.
    """
    try:
        EspacoService.delete(int(id))
        return {"message": "Espaço deletado com sucesso."}
    except NotFoundException:
        response.status_code = 404
        return {"error": "Espaço não encontrado."}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

from fastapi import APIRouter, Response
from app.domain.pagamento import PagamentoRequest, PagamentoDBSchema
from app.service.pagamento import PagamentoService, NotFoundException

pagamento_router = APIRouter(prefix="/pagamento", tags=["Pagamento"])

@pagamento_router.get("/")
def read(response: Response):
    """
    Retorna todos os pagamentos cadastrados.
    """
    try:
        pagamentos = PagamentoService.read_all()
        return pagamentos
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

@pagamento_router.get("/{id}")
def read_id(id: str, response: Response):
    """
    Retorna um pagamento específico pelo ID.
    """
    try:
        pagamento = PagamentoService.read_by_id(int(id))
        return pagamento
    except NotFoundException:
        response.status_code = 404
        return {"error": "Pagamento não encontrado."}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

@pagamento_router.put("/{id}")
def update(id: str, input: PagamentoRequest, response: Response):
    """
    Atualiza os dados de um pagamento existente.
    """
    try:
        pagamento = PagamentoService.update(int(id), input)
        return pagamento
    except NotFoundException:
        response.status_code = 404
        return {"error": "Pagamento não encontrado."}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

@pagamento_router.delete("/{id}")
def delete(id: str, response: Response):
    """
    Remove um pagamento pelo ID.
    """
    try:
        PagamentoService.delete(int(id))
        return {"message": "Pagamento deletado com sucesso."}
    except NotFoundException:
        response.status_code = 404
        return {"error": "Pagamento não encontrado."}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

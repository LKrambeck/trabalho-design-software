from fastapi import APIRouter, Response
from app.domain.usuario import UsuarioRequest, UsuarioDBSchema
from app.service.usuario import UsuarioService, NotFoundException

usuario_router = APIRouter(prefix="/usuario", tags=["Usuário"])

@usuario_router.post("/")
def create(input: UsuarioRequest, response: Response):
    """
    Cria um novo usuário.
    """
    try:
        usuario = UsuarioService.create(input)
        response.status_code = 201
        return usuario
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

@usuario_router.get("/")
def read(response: Response):
    """
    Retorna todos os usuários cadastrados.
    """
    try:
        usuarios = UsuarioService.read_all()
        return usuarios
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

@usuario_router.get("/{id}")
def read_id(id: str, response: Response):
    """
    Retorna um usuário específico pelo ID.
    """
    try:
        usuario = UsuarioService.read_by_id(int(id))
        return usuario
    except NotFoundException:
        response.status_code = 404
        return {"error": "Usuário não encontrado."}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

@usuario_router.put("/{id}")
def update(id: str, input: UsuarioRequest, response: Response):
    """
    Atualiza os dados de um usuário existente.
    """
    try:
        usuario = UsuarioService.update(int(id), input)
        return usuario
    except NotFoundException:
        response.status_code = 404
        return {"error": "Usuário não encontrado."}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

@usuario_router.delete("/{id}")
def delete(id: str, response: Response):
    """
    Remove um usuário pelo ID.
    """
    try:
        UsuarioService.delete(int(id))
        return {"message": "Usuário deletado com sucesso."}
    except NotFoundException:
        response.status_code = 404
        return {"error": "Usuário não encontrado."}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}

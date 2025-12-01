from domain.usuario import UsuarioRequest
from repository.usuario import UsuarioRepository, UsuarioDBSchema

class NotFoundException(Exception):
    pass

class UsuarioService:
    def create(input: UsuarioRequest) -> UsuarioDBSchema:
        db = UsuarioRepository.read_all()
        for usuario in db:
            if usuario.email == input.email:
                raise Exception("Email ja cadastrado")

        usuario = UsuarioRepository.create(input)
        return usuario.dict()

    def read_all() -> list[UsuarioDBSchema]:
        return UsuarioRepository.read_all()

    def read_by_id(usuario_id: int) -> UsuarioDBSchema | None:
        if usuario := UsuarioRepository.read_by_id(usuario_id):
            return usuario.dict()
        raise NotFoundException()

    def update(usuario_id: int, updated_usuario: UsuarioRequest) -> UsuarioDBSchema | None:
        usuario_schema = UsuarioDBSchema(**updated_usuario.dict(), id=usuario_id)
        usuarios = UsuarioRepository.read_all()
        for usuario in usuarios:
            if usuario.email == updated_usuario.email and usuario.id != usuario_id:
                raise Exception("Email ja cadastrado")

        if usuario := UsuarioRepository.update(usuario_id, usuario_schema):
            return usuario.dict()
        raise NotFoundException()

    def delete(usuario_id: int):
        if not UsuarioRepository.delete(usuario_id):
            raise NotFoundException()

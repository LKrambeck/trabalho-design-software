from domain.usuario import UsuarioDBSchema, UsuarioRequest
from typing import List, Optional
from json import dump, load
import os

DB_FILE_PATH = "src/app/repository/db/usuario.json"

def read_db() -> List[UsuarioDBSchema]:
    """Read the whole usuario DB file and return parsed Pydantic models.

    Returns an empty list if the file does not exist or is empty.
    """
    if not os.path.exists(DB_FILE_PATH):
        return []
    with open(DB_FILE_PATH, "r") as f:
        try:
            raw = load(f)
        except Exception:
            return []
    return [UsuarioDBSchema(**item) for item in raw]

def write_db(data: List[UsuarioDBSchema]):
    """Write the list of Pydantic models to the DB file as JSON.

    Ensures parent directory exists.
    """
    data_to_insert = [item.dict() for item in data]
    os.makedirs(os.path.dirname(DB_FILE_PATH), exist_ok=True)
    with open(DB_FILE_PATH, "w") as f:
        dump(data_to_insert, f, indent=4)

class UsuarioRepository:

    def create(usuario: UsuarioRequest) -> UsuarioDBSchema:
        usuario_id = max((item.id for item in read_db()), default=0) + 1
        usuario_insert = UsuarioDBSchema(**usuario.dict(), id=usuario_id)
        db = read_db()

        db.append(usuario_insert)
        write_db(db)

        return usuario_insert

    def read_all() -> List[UsuarioDBSchema]:
        return read_db()

    def read_by_id(usuario_id: int) -> Optional[UsuarioDBSchema]:
        for usuario in read_db():
            if usuario.id == usuario_id:
                return usuario
        return None

    def update(usuario_id: int, updated_usuario: UsuarioDBSchema) -> Optional[UsuarioDBSchema]:
        db = read_db()
        for index, usuario in enumerate(db):
            if usuario.id == usuario_id:
                updated_usuario.id = usuario_id
                db[index] = updated_usuario
                write_db(db)
                return updated_usuario
        return None

    def delete(usuario_id: int) -> bool:
        db = read_db()
        for index, usuario in enumerate(db):
            if usuario.id == usuario_id:
                del db[index]
                write_db(db)
                return True
        return False

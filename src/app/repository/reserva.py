from app.domain.reserva import ReservaDBSchema, ReservaRequest
from datetime import date
from typing import List, Optional
from json import dump, load
import os

DB_FILE_PATH = "src/app/repository/db/reserva.json"

def read_db() -> List[ReservaDBSchema]:
    """Read the whole reserva DB file and return parsed Pydantic models.

    Returns an empty list if the file does not exist or is empty.
    """
    if not os.path.exists(DB_FILE_PATH):
        return []
    with open(DB_FILE_PATH, "r") as f:
        try:
            raw = load(f)
        except Exception:
            return []

    # Converte strings de data de volta para objetos date
    res = []
    for item in raw:
        item["data_inicio"] = date.fromisoformat(item["data_inicio"])
        item["data_fim"] = date.fromisoformat(item["data_fim"])
        res.append(ReservaDBSchema(**item))

    return res

def write_db(data: List[ReservaDBSchema]):
    """Write the list of Pydantic models to the DB file as JSON.

    Ensures parent directory exists.
    """
    data_to_insert = [item.dict() for item in data]
    for item in data_to_insert:
        item["data_inicio"] = item["data_inicio"].isoformat()
        item["data_fim"] = item["data_fim"].isoformat()

    os.makedirs(os.path.dirname(DB_FILE_PATH), exist_ok=True)
    with open(DB_FILE_PATH, "w") as f:
        dump(data_to_insert, f, indent=4)

class ReservaRepository:

    def create(reserva: dict) -> ReservaDBSchema:
        reserva_id = max((item.id for item in read_db()), default=0) + 1
        reserva_insert = ReservaDBSchema(**reserva, id=reserva_id)
        db = read_db()

        db.append(reserva_insert)
        write_db(db)

        return reserva_insert

    def read_all() -> List[ReservaDBSchema]:
        return read_db()

    def read_by_id(reserva_id: int) -> Optional[ReservaDBSchema]:
        for reserva in read_db():
            if reserva.id == reserva_id:
                return reserva
        return None

    def update(reserva_id: int, updated_reserva: ReservaDBSchema) -> Optional[ReservaDBSchema]:
        db = read_db()
        for index, reserva in enumerate(db):
            if reserva.id == reserva_id:
                updated_reserva.id = reserva_id
                db[index] = updated_reserva
                write_db(db)
                return updated_reserva
        return None

    def delete(reserva_id: int) -> bool:
        db = read_db()
        for index, reserva in enumerate(db):
            if reserva.id == reserva_id:
                del db[index]
                write_db(db)
                return True
        return False

from domain.espaco import EspacoDBSchema, EspacoRequest
from typing import List, Optional
from json import dump, load
import os

DB_FILE_PATH = "src/app/repository/db/espaco.json"


def read_db() -> List[EspacoDBSchema]:
    """Read the whole espaco DB file and return parsed Pydantic models.

    Returns an empty list if the file does not exist or is empty.
    """
    if not os.path.exists(DB_FILE_PATH):
        return []
    with open(DB_FILE_PATH, "r") as f:
        try:
            raw = load(f)
        except Exception:
            return []
    return [EspacoDBSchema(**item) for item in raw]


def write_db(data: List[EspacoDBSchema]):
    """Write the list of Pydantic models to the DB file as JSON.

    Ensures parent directory exists.
    """
    data_to_insert = [item.dict() for item in data]
    os.makedirs(os.path.dirname(DB_FILE_PATH), exist_ok=True)
    with open(DB_FILE_PATH, "w") as f:
        dump(data_to_insert, f, indent=4)


class EspacoRepository:

    def create(espaco: EspacoRequest) -> EspacoDBSchema:
        espaco_id = max((item.id for item in read_db()), default=0) + 1
        espaco_insert = EspacoDBSchema(**espaco.dict(), id=espaco_id)
        db = read_db()

        db.append(espaco_insert)
        write_db(db)

        return espaco_insert

    def read_all() -> List[EspacoDBSchema]:
        # always read fresh data
        return read_db()

    def read_by_id(espaco_id: int) -> Optional[EspacoDBSchema]:
        for espaco in read_db():
            if espaco.id == espaco_id:
                return espaco
        return None

    def update(espaco_id: int, updated_espaco: EspacoDBSchema) -> Optional[EspacoDBSchema]:
        db = read_db()
        for index, espaco in enumerate(db):
            if espaco.id == espaco_id:
                updated_espaco.id = espaco_id
                db[index] = updated_espaco
                write_db(db)
                return updated_espaco
        return None

    def delete(espaco_id: int) -> bool:
        db = read_db()
        for index, espaco in enumerate(db):
            if espaco.id == espaco_id:
                del db[index]
                write_db(db)
                return True
        return False
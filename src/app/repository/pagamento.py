from datetime import datetime
from domain.pagamento import PagamentoDBSchema, PagamentoRequest
from typing import List, Optional
from json import dump, load
import os

DB_FILE_PATH = "src/app/repository/db/pagamento.json"

def read_db() -> List[PagamentoDBSchema]:
    """Read the whole pagamento DB file and return parsed Pydantic models.

    Returns an empty list if the file does not exist or is empty.
    """
    if not os.path.exists(DB_FILE_PATH):
        return []
    with open(DB_FILE_PATH, "r") as f:
        try:
            raw = load(f)
        except Exception:
            return []

    # Converte strings de data de volta para objetos datetime
    res = []
    for item in raw:
        item["data_pagamento"] = datetime.fromisoformat(item["data_pagamento"])
        res.append(PagamentoDBSchema(**item))

    return res

def write_db(data: List[PagamentoDBSchema]):
    """Write the list of Pydantic models to the DB file as JSON.

    Ensures parent directory exists.
    """
    data_to_insert = [item.dict() for item in data]
    for item in data_to_insert:
        item["data_pagamento"] = item["data_pagamento"].isoformat()
    
    os.makedirs(os.path.dirname(DB_FILE_PATH), exist_ok=True)
    with open(DB_FILE_PATH, "w") as f:
        dump(data_to_insert, f, indent=4)

class PagamentoRepository:

    def create(pagamento: PagamentoRequest) -> PagamentoDBSchema:
        pagamento_id = max((item.id for item in read_db()), default=0) + 1
        pagamento_insert = PagamentoDBSchema(
            **pagamento.dict(),
            id=pagamento_id,
            data_pagamento=datetime.now(),
            status="sinal"
        )
        db = read_db()

        db.append(pagamento_insert)
        write_db(db)

        return pagamento_insert

    def read_all() -> List[PagamentoDBSchema]:
        return read_db()

    def read_by_id(pagamento_id: int) -> Optional[PagamentoDBSchema]:
        for pagamento in read_db():
            if pagamento.id == pagamento_id:
                return pagamento
        return None

    def update(pagamento_id: int, updated_pagamento: PagamentoDBSchema) -> Optional[PagamentoDBSchema]:
        db = read_db()
        for index, pagamento in enumerate(db):
            if pagamento.id == pagamento_id:
                updated_pagamento.id = pagamento_id
                db[index] = updated_pagamento
                write_db(db)
                return updated_pagamento
        return None

    def delete(pagamento_id: int) -> bool:
        db = read_db()
        for index, pagamento in enumerate(db):
            if pagamento.id == pagamento_id:
                del db[index]
                write_db(db)
                return True
        return False

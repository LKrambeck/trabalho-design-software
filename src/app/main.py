from fastapi import FastAPI
from app.routers.espaco import espaco_router
from app.routers.usuario import usuario_router
from app.routers.pagamento import pagamento_router
from app.routers.reserva import reserva_router

app = FastAPI(title="Meu cantinho", version="1.0.0")

app.include_router(espaco_router)
app.include_router(usuario_router)
app.include_router(pagamento_router)
app.include_router(reserva_router)
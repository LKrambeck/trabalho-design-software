from fastapi import FastAPI
from routers.espaco import espaco_router
from routers.usuario import usuario_router
from routers.pagamento import pagamento_router
from routers.reserva import reserva_router

app = FastAPI(title="Meu cantinho", version="1.0.0")

app.include_router(espaco_router)
app.include_router(usuario_router)
app.include_router(pagamento_router)
app.include_router(reserva_router)
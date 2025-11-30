from fastapi import FastAPI

app = FastAPI(title="Meu cantinho", version="1.0.0")
@app.get("/")
def read_root():
    return {"message": "Welcome to Meu cantinho!"}

@app.get("/status")
def read_status(status: str = "ok"):
    """
    lepo lepo
    """
    return {"status": "ok"}
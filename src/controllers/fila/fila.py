from fastapi import APIRouter

from src.schemas.fila import CriarFila

fila_router = APIRouter()


@fila_router.get("/fila")
async def obter_fila():
    return {"filas": []}


@fila_router.get("/fila/{_id}")
async def obter_fila_id(_id: int):
    ...


@fila_router.post("/fila")
async def criar_fila(request: CriarFila):
    ...


@fila_router.put("/fila")
async def atualizar_fila():
    ...


@fila_router.delete("/fila/{_id}")
async def excluir_fila(_id: int):
    ...

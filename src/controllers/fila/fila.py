from fastapi import APIRouter

from src.schemas.fila import CriarFila
from src.schemas.fila import Fila

fila_router = APIRouter()
db_fila = []

def obter_fila_nao_atendidos():
    _fila = [x for x in db_fila if x.atendido == False]
    return _fila;

@fila_router.get("/fila")
async def get_fila():
    _ret = obter_fila_nao_atendidos();
    if(len(_ret) > 0):
        return {"filas": _ret}
    return {}


@fila_router.get("/fila/{_id}")
async def obter_fila_id(_id: int):
    ...
async def get_fila_id(_id: str):
    _fila = [x for x in obter_fila_nao_atendidos() if x.id == _id]
    return {"fila": _fila}


@fila_router.post("/fila")
async def criar_fila(request: CriarFila):
    ...


@fila_router.put("/fila")
async def atualizar_fila():
    ...


@fila_router.delete("/fila/{_id}")
async def excluir_fila(_id: int):
    ...

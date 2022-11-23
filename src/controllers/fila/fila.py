import uuid
from fastapi import APIRouter

from src.schemas.fila import Fila
from src.schemas.request.fila import Post_fila
from src.schemas.response.fila import Get_fila

fila_router = APIRouter()
db_fila = []

def obter_fila_nao_atendidos():
    _fila = [x for x in db_fila if x.atendido == False]
    return _fila;

@fila_router.get("/fila")
async def get_fila():
    _ret = obter_fila_nao_atendidos();
    if(len(_ret) > 0):
        _fila = _ret.apply()
        return {"filas": _ret}
    return {}


@fila_router.get("/fila/{_id}")
async def obter_fila_id(_id: int):
    ...
async def get_fila_id(_id: str):
    _fila = [x for x in obter_fila_nao_atendidos() if x.id == _id]
    return {"fila": _fila}


@fila_router.post("/fila")
async def post_fila(request: Post_fila):
    _fila = Fila(id=str(uuid.uuid4()),posicao=len(db_fila)+1, nome_cliente=request.nome_cliente, atendimento=request.atendimento)
    db_fila.append(_fila)
    return {"fila": _fila}

@fila_router.put("/fila")
async def put_fila():
    ...


@fila_router.delete("/fila/{_id}")
async def delete_fila(_id: str):
    ...

from typing import List
import uuid
from fastapi import APIRouter, Response, status
from datetime import datetime
from src.schemas.fila import Fila
from src.schemas.request.fila import Post_fila
from src.schemas.response.fila import Get_fila

fila_router = APIRouter()


class database:
    fila: List = []


def obter_fila_nao_atendidos():
    _fila = [x for x in database.fila if x.atendido == False]
    return _fila


def obter_fila_atendidos():
    _fila = [x for x in database.fila if x.atendido == True]
    return _fila


def atualizar_fila(startIndex: int = 0):
    for cliente in (
        database.fila[startIndex : len(database.fila)]
        if startIndex > 0
        else database.fila
    ):
        if cliente.posicao == 1:
            cliente.atendido = True
            cliente.data_entrada = datetime.now()

        if cliente.posicao != 0:
            cliente.posicao -= 1


def obter_fila_por_id(id: str):
    _fila = next(filter(lambda x: x.id == id, database.fila), None)
    return _fila


@fila_router.get("/fila/atendidos")
async def get_fila():
    _ret = obter_fila_atendidos()
    if len(_ret) > 0:
        return {"filas": _ret}
    return {}


@fila_router.get("/fila")
async def get_fila():
    _ret = obter_fila_nao_atendidos()
    if len(_ret) > 0:
        return {"filas": _ret}
    return {}


@fila_router.get("/fila/{_id}")
async def get_fila_id(_id: str, response: Response):
    _fila = obter_fila_por_id(_id)
    if _fila != None:
        return {"fila": _fila}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Mensagem": "Não foi encontrado a fila solicitada."}


@fila_router.post("/fila")
async def post_fila(request: Post_fila):
    _fila = Fila(
        id=str(uuid.uuid4()),
        posicao=len(database.fila) + 1,
        nome_cliente=request.nome_cliente,
        atendimento=request.atendimento,
    )
    database.fila.append(_fila)
    return {"fila": _fila}


@fila_router.put("/fila")
async def put_fila():
    atualizar_fila()
    return {"Mensagem": "Fila atualizada com sucesso!"}


@fila_router.delete("/fila/{_id}")
async def delete_fila(_id: str, response: Response):
    _fila = obter_fila_por_id(_id)

    if _fila == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Mensagem": "Não foi encontrado a fila solicitada."}

    fila_index = database.fila.index(_fila)
    database.fila.remove(_fila)
    atualizar_fila(fila_index)

    if obter_fila_por_id(_id) == None:
        return {"Mensagem": "Removido com sucesso"}

    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"Mensagem": "Não foi possível remover."}

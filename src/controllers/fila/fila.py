from typing import List
import uuid
from fastapi import APIRouter, Response, status
from datetime import datetime
from src.schemas.fila import Atendimento, Fila
from src.schemas.request.fila import Post_fila
from src.schemas.response.fila import Get_fila

fila_router = APIRouter()


class database:
    fila: List = []


def obter_fila_nao_atendidos():
    _fila = [x for x in database.fila if x.atendido == False]
    _fila.sort(key=lambda x: x.posicao)
    return _fila


def obter_fila_atendidos():
    _fila = [x for x in database.fila if x.atendido == True]
    _fila.sort(key=lambda x: x.posicao)
    return _fila


def atualizar_fila(startIndex: int = 0):
    for cliente in (
        obter_fila_nao_atendidos()[startIndex : len(database.fila)]
        if startIndex > 0
        else obter_fila_nao_atendidos()
    ):
        if cliente.posicao == 1:
            cliente.atendido = True
            cliente.data_entrada = datetime.now()

        if cliente.posicao != 0:
            cliente.posicao -= 1


def inserir_fila(fila: Post_fila):
    next_position = 1
    if fila.atendimento == Atendimento.Normal:
        fila_max = max(database.fila, key=lambda x: x.posicao, default=None)
        if fila_max != None:
            next_position = fila_max.posicao + 1

    if fila.atendimento == Atendimento.Prioritario:
        fila_max = max(
            [
                x
                for x in obter_fila_nao_atendidos()
                if x.atendimento == Atendimento.Prioritario
            ],
            key=lambda x: x.posicao,
            default=None,
        )
        next_position = 1 if fila_max == None else fila_max.posicao + 1
        for cliente in obter_fila_nao_atendidos()[
            next_position - 1 : len(database.fila)
        ]:
            if cliente.posicao != 0:
                cliente.posicao += 1

    _fila = Fila(
        id=str(uuid.uuid4()),
        posicao=next_position,
        nome_cliente=fila.nome_cliente,
        atendimento=fila.atendimento,
    )
    database.fila.append(_fila)
    return _fila


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
    _fila = inserir_fila(request)
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

    database.fila.remove(_fila)
    atualizar_fila(_fila.posicao - 1)

    if obter_fila_por_id(_id) == None:
        return {"Mensagem": "Removido com sucesso"}

    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"Mensagem": "Não foi possível remover."}

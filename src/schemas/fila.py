from typing import Optional
from pydantic import BaseModel, constr
from datetime import datetime
from enum import Enum


class Atendimento(Enum):
    Normal = "N"
    Prioritario = "P"


class Fila(BaseModel):
    id: Optional[int] = 0
    posicao: Optional[int] = None
    nome_cliente: Optional[constr(max_length=10)]
    data_chegada: Optional[datetime] = datetime.now()
    data_entrada: Optional[datetime] = False
    atendimento: Optional[Atendimento] = Atendimento.Normal
    atendido: Optional[bool] = False


class CriarFila(BaseModel):
    nome_cliente: Optional[constr(max_length=10)]
    atendimento: Optional[Atendimento] = Atendimento.Normal

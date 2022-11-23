from typing import Optional
from pydantic import BaseModel, constr
from datetime import datetime
from enum import Enum
import uuid


class Atendimento(Enum):
    Normal = "N"
    Prioritario = "P"


class Fila(BaseModel):
    id: str
    posicao: Optional[int] = None
    nome_cliente: Optional[constr(max_length=20)]
    data_chegada: Optional[datetime] = datetime.now()
    data_entrada: Optional[datetime] = False
    atendimento: Optional[Atendimento] = Atendimento.Normal
    atendido: Optional[bool] = False


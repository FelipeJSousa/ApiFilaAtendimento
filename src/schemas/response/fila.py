from typing import Optional
from pydantic import BaseModel, constr
from datetime import datetime
from enum import Enum
import uuid

from src.schemas.fila import Atendimento

class Get_fila(BaseModel):
    id: str
    posicao: Optional[int] = None
    nome_cliente: Optional[constr(max_length=10)]
    data_chegada: Optional[datetime] = datetime.now()
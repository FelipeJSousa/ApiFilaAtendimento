from typing import Optional
from pydantic import BaseModel, constr

from src.schemas.fila import Atendimento

class Post_fila(BaseModel):
    nome_cliente: Optional[constr(max_length=20)]
    atendimento: Optional[Atendimento] = Atendimento.Normal
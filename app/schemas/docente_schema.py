from typing import Optional
from pydantic import BaseModel, ConfigDict

class DocenteCrear(BaseModel):
    id_usuario: int
    id_unidad: int

class DocenteActualizar(BaseModel):
    id_usuario: Optional[int] = None
    id_unidad: Optional[int] = None
    model_config = {"extra": "ignore"}

class DocenteRead(BaseModel):
    id_docente: int
    id_usuario: int
    id_unidad: int

    model_config = ConfigDict(from_attributes=True)
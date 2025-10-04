from pydantic import BaseModel, ConfigDict
from typing import Optional

class EstudianteCrear(BaseModel):
    id_usuario: int
    id_programa: int

class EstudianteActualizar(BaseModel):
    id_usuario: Optional[int] = None
    id_programa: Optional[int] = None
    model_config = {"extra": "ignore"}

class EstudianteRead(BaseModel):
    id_estudiante: int
    id_usuario: int
    id_programa: int

    model_config = ConfigDict(from_attributes=True)
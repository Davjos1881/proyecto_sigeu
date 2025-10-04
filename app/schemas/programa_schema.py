from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class ProgramaCrear(BaseModel):
    nombre_programa: str = Field(..., min_length=1, max_length=100)
    id_facultad: int

class ProgramaActualizar(BaseModel):
    nombre_programa: Optional[str] = None
    id_facultad: Optional[int] = None
    model_config = {"extra": "ignore"}

class ProgramaRead(BaseModel):
    id_programa: int
    nombre_programa: str
    id_facultad: int

    model_config = ConfigDict(from_attributes=True)
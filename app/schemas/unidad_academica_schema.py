from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class UnidadAcademicaCrear(BaseModel):
    nombre_unidad: str = Field(..., min_length=1, max_length=100)
    id_facultad: int

class UnidadAcademicaActualizar(BaseModel):
    nombre_unidad: Optional[str] = None
    id_facultad: Optional[int] = None
    model_config = {"extra": "ignore"}

class UnidadAcademicaRead(BaseModel):
    id_unidad: int
    nombre_unidad: str
    id_facultad: int

    model_config = ConfigDict(from_attributes=True)
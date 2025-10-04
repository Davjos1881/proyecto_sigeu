from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class FacultadCrear(BaseModel):
    nombre_facultad: str = Field(..., min_length=1, max_length=100)

class FacultadActualizar(BaseModel):
    nombre_facultad: Optional[str] = None
    model_config = {"extra": "ignore"}

class FacultadRead(BaseModel):
    id_facultad: int
    nombre_facultad: str

    model_config = ConfigDict(from_attributes=True)
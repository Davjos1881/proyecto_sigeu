from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class SecretarioCrear(BaseModel):
    nombre_secretario: str = Field(..., min_length=1, max_length=100)
    id_unidad: int

class SecretarioActualizar(BaseModel):
    nombre_secretario: Optional[str] = None
    id_unidad: Optional[int] = None
    model_config = {"extra": "ignore"}

class SecretarioRead(BaseModel):
    id_secretaria: int
    nombre_secretario: str
    id_unidad: int

    model_config = ConfigDict(from_attributes=True)
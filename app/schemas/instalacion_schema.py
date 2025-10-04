from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class InstalacionBase(BaseModel):
    nombre_instalacion: str = Field(..., min_length=1, max_length=100)
    ubicacion: Optional[str] = Field(None, max_length=200)
    tipo_instalacion: Optional[str] = Field(None, max_length=100)

class InstalacionCrear(InstalacionBase):
    pass

class InstalacionActualizar(BaseModel):
    nombre_instalacion: Optional[str] = None
    ubicacion: Optional[str] = None
    tipo_instalacion: Optional[str] = None

    model_config = {"extra": "ignore"}

class InstalacionRead(InstalacionBase):
    id_instalacion: int

    model_config = ConfigDict(from_attributes=True)
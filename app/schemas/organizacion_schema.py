from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

class OrganizacionBase(BaseModel):
    nombre_organizacion: str = Field(..., min_length=1, max_length=100)
    representante_legal: str = Field(..., min_length=1, max_length=100)
    es_representante_externo: Optional[bool] = False
    telefono: Optional[str] = Field(None, max_length=45)
    direccion: Optional[str] = Field(None, max_length=200)
    actividad: Optional[str] = Field(None, max_length=100)
    sector_economico: Optional[str] = Field(None, max_length=100)

class OrganizacionCrear(OrganizacionBase):
    pass

class OrganizacionRead(OrganizacionBase):
    id_organizacion: int

    model_config = ConfigDict(from_attributes=True)

class OrganizacionActualizar(BaseModel):
    # todos opcionales para updates parciales
    nombre_organizacion: Optional[str] = None
    representante_legal: Optional[str] = None
    es_representante_externo: Optional[bool] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    actividad: Optional[str] = None
    sector_economico: Optional[str] = None

    model_config = {"extra": "ignore"}
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date

class CertificadoCrear(BaseModel):
    organizacion_id_organizacion: int
    representante: str = Field(..., min_length=1, max_length=100)
    fecha_emision: Optional[date] = None
    descripcion: Optional[str] = None

class CertificadoActualizar(BaseModel):
    organizacion_id_organizacion: Optional[int] = None
    representante: Optional[str] = None
    fecha_emision: Optional[str] = None
    model_config = {"extra": "ignore"}

class CertificadoRead(BaseModel):
    id_certificado: int
    organizacion_id_organizacion: int
    representante: str
    fecha_emision: Optional[date]
    descripcion: Optional[str]

    model_config = ConfigDict(from_attributes=True)
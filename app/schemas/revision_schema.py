from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date

class RevisionCrear(BaseModel):
    id_evento: int
    id_secretario: int
    estado: str = Field("en espera", min_length=1, max_length=20)  # aprobado|rechazado|en espera
    fecha_revision: Optional[date] = None
    justificacion: Optional[str] = None
    usuario_id_usuario: int

class RevisionActualizar(BaseModel):
    id_evento: Optional[int] = None
    id_secretario: Optional[int] = None
    estado: Optional[str] = None
    fecha_revision: Optional[date] = None
    justificacion: Optional[str] = None
    usuario_id_usuario: Optional[int] = None
    model_config = {"extra": "ignore"}

class RevisionRead(BaseModel):
    id_revision: int
    id_evento: int
    id_secretario: int
    estado: str
    fecha_revision: Optional[date]
    justificacion: Optional[str]
    usuario_id_usuario: int

    model_config = ConfigDict(from_attributes=True)
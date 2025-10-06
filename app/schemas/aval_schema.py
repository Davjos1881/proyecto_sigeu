from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date

class AvalCrear(BaseModel):
    evento_id_evento: int
    id_unidad: int
    usuario_id_usuario: int

    nombre_responsable: str = Field(..., min_length=1, max_length=100)
    rol_responsable: str = Field(..., min_length=1, max_length=20)
    fecha_emision: Optional[date] = None
    emitido_por: Optional[str] = None
    descripcion: Optional[str] = None


class AvalEventoActualizar(BaseModel):
    evento_id_evento: Optional[int] = None
    id_unidad: Optional[int] = None
    usuario_id_usuario: Optional[int] = None
    nombre_responsable: Optional[str] = None
    rol_responsable: Optional[str] = None
    fecha_emision: Optional[date] = None
    emitido_por: Optional[str] = None

    model_config = {"extra": "ignore"}

class AvalRead(BaseModel):
    id_aval: int
    evento_id_evento: int
    id_unidad: int
    usuario_id_usuario: int
    nombre_responsable: str
    rol_responsable: str
    fecha_emision: Optional[date]
    emitido_por: Optional[str]

    model_config = ConfigDict(from_attributes=True)
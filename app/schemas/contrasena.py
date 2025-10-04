from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date

class ContrasenaCrear(BaseModel):
    usuario_id_usuario: int
    fecha_creacion: date
    fecha_ultimo_cambio: date
    esta_vigente: bool = True

class ContrasenaActualizar(BaseModel):
    usuario_id_usuario: Optional[int] = None
    fecha_creacion: Optional[date] = None
    fecha_ultimo_cambio: Optional[date] = None
    esta_vigente: Optional[bool] = None
    model_config = {"extra": "ignore"}

class ContrasenaRead(BaseModel):
    id_contraseña: int = Field(..., alias="id_contraseña")
    usuario_id_usuario: int
    fecha_creacion: date
    fecha_ultimo_cambio: date
    esta_vigente: bool

    model_config = ConfigDict(from_attributes=True)
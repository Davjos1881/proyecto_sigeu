from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date

class NotificacionCrear(BaseModel):
    id_usuario: int
    evento_id_evento: Optional[int] = None
    mensaje: str = Field(..., min_length=1)
    fecha_envio: Optional[date] = None

class NotificacionActualizar(BaseModel):
    id_usuario: Optional[int] = None
    evento_id_evento: Optional[int] = None
    mensaje: Optional[str] = None
    fecha_envio: Optional[date] = None
    model_config = {"extra": "ignore"}


class NotificacionRead(BaseModel):
    id_notificacion: int
    id_usuario: int
    evento_id_evento: Optional[int]
    mensaje: str
    fecha_envio: Optional[date]

    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, List
from datetime import date
from app.schemas.aval_schema import AvalRead
from app.schemas.revision_schema import RevisionRead
from app.schemas.notificacion_schema import NotificacionRead
from app.schemas.certificado_schema import CertificadoRead

class EventoBase(BaseModel):
    id_organizacion: Optional[int] = None
    id_instalacion: int
    id_certificado_participacion: Optional[int] = None

    titulo: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None

    fecha_creacion: Optional[date] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

    publicado: Optional[bool] = False

    aval_presente: Optional[bool] = False
    aval_descripcion: Optional[str] = None

    certificado_presente: Optional[bool] = False
    certificado_descripcion: Optional[str] = None

    acta_presente: Optional[bool] = False
    acta_descripcion: Optional[str] = None

    @field_validator("fecha_fin")
    @classmethod
    def validar_fin_no_menor_que_inicio(cls, v, info):
        """
        Permite fechas futuras. Solo valida que, si ambos estan presentes,
        fecha_fin >= fecha_inicio.
        """
        fecha_inicio = info.data.get("fecha_inicio")
        if fecha_inicio and v and v < fecha_inicio:
            raise ValueError("fecha_fin no puede ser anterior a fecha_inicio")
        return v

class EventoCrear(EventoBase):
    pass

class EventoRead(EventoBase):
    id_evento: int
    avales: Optional[List[AvalRead]] = []
    revisiones: Optional[List[RevisionRead]] = []
    notificaciones: Optional[List[NotificacionRead]] = []
    certificado: Optional[CertificadoRead] = None

    model_config = ConfigDict(from_attributes=True)

class EventoActualizar(BaseModel):
    titulo: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    publicado: Optional[bool] = None
    id_instalacion: Optional[int] = None
    id_organizacion: Optional[int] = None
    id_certificado_participacion: Optional[int] = None
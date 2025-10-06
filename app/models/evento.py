from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.mysql import Base
from app.models.organizacion import OrganizacionExterna
from app.models.instalacion import Instalacion
from app.models.certificado import CertificadoParticipacion
from app.models.aval import AvalEvento
from app.models.revision import Revision
from app.models.notificacion import Notificacion

class Evento(Base):
    __tablename__ = "evento"

    id_evento = Column(Integer, primary_key=True, autoincrement=True)
    id_organizacion = Column(Integer, ForeignKey("organizacion_externa.id_organizacion"), nullable=True)
    id_instalacion = Column(Integer, ForeignKey("instalacion.id_instalacion"), nullable=False)
    id_certificado_participacion = Column(Integer, ForeignKey("certificado_participacion.id_certificado"), nullable=True)

    titulo = Column(String(200), nullable=False)
    fecha_creacion = Column(Date, nullable=False)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    publicado = Column(Boolean, default=False)

    organizacion = relationship("OrganizacionExterna", back_populates="eventos", lazy="selectin")
    instalacion = relationship("Instalacion", back_populates="eventos", lazy="selectin")
    certificado = relationship("CertificadoParticipacion", back_populates="evento", uselist=False, lazy="selectin")
    avales = relationship("AvalEvento", back_populates="evento", lazy="selectin")
    revisiones = relationship("Revision", back_populates="evento", lazy="selectin")
    notificaciones = relationship("Notificacion", back_populates="evento", lazy="selectin")
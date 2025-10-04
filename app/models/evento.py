from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.mysql import Base

class Evento(Base):
    __tablename__ = "evento"

    id_evento = Column(Integer, primary_key=True, autoincrement=True)
    id_organizacion = Column(Integer, ForeignKey("organizacion_externa.id_organizacion"), nullable=True)
    id_instalacion = Column(Integer, ForeignKey("instalacion.id_instalacion"), nullable=False)
    id_certificado_participacion = Column(Integer, ForeignKey("certificado_participacion.id_certificado"), nullable=True)

    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(Date, nullable=False)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    publicado = Column(Boolean, default=False)

    # metadatos en lugar de archivos reales
    aval_presente = Column(Boolean, default=False)
    aval_descripcion = Column(Text, nullable=True)

    certificado_presente = Column(Boolean, default=False)
    certificado_descripcion = Column(Text, nullable=True)

    acta_presente = Column(Boolean, default=False)
    acta_descripcion = Column(Text, nullable=True)

    organizacion = relationship("OrganizacionExterna", back_populates="eventos")
    instalacion = relationship("Instalacion", back_populates="eventos")
    certificado = relationship("CertificadoParticipacion", back_populates="evento", uselist=False)
    avales = relationship("AvalEvento", back_populates="evento")
    revisiones = relationship("Revision", back_populates="evento")
    notificaciones = relationship("Notificacion", back_populates="evento")
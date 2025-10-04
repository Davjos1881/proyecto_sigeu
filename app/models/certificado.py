from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base

class CertificadoParticipacion(Base):
    __tablename__ = "certificado_participacion"

    id_certificado = Column(Integer, primary_key=True, autoincrement=True)
    organizacion_id_organizacion = Column(Integer, ForeignKey("organizacion_externa.id_organizacion"), nullable=False)
    representante = Column(String(100), nullable=False)
    fecha_emision = Column(String(45), nullable=True)
    descripcion = Column(Text, nullable=True)

    organizacion = relationship("OrganizacionExterna", back_populates="certificados")
    evento = relationship("Evento", back_populates="certificado", uselist=False)
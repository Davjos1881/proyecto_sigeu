from app.db.mysql import Base
from sqlalchemy import Integer, Column, String, Boolean
from sqlalchemy.orm import relationship

class OrganizacionExterna(Base):
    __tablename__ = "organizacion_externa"

    id_organizacion = Column(Integer, primary_key=True, autoincrement=True)
    nombre_organizacion = Column(String(100), nullable=False, unique=True)
    representante_legal = Column(String(100), nullable=False)
    es_representante_externo = Column(Boolean, nullable=True, default=False)
    telefono = Column(String(45), nullable=True)
    direccion = Column(String(200), nullable=True)
    actividad = Column(String(100), nullable=True)
    sector_economico = Column(String(100), nullable=True)

    certificados = relationship("CertificadoParticipacion", back_populates="organizacion")
    eventos = relationship("Evento", back_populates="organizacion")
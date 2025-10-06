from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base
from app.models.facultad import Facultad 
from app.models.secretario_academico import SecretarioAcademico

class UnidadAcademica(Base):
    __tablename__ = "unidad_academica"

    id_unidad = Column(Integer, primary_key=True, autoincrement=True)
    nombre_unidad = Column(String(100), nullable=False)
    id_facultad = Column(Integer, ForeignKey("facultad.id_facultad"), nullable=False)

    facultad = relationship("Facultad", back_populates="unidades")
    docentes = relationship("Docente", back_populates="unidad")
    secretarios = relationship("SecretarioAcademico", back_populates="unidad")
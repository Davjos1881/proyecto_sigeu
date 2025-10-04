from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base

class Docente(Base):
    __tablename__ = "docente"

    id_docente = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_unidad = Column(Integer, ForeignKey("unidad_academica.id_unidad"), nullable=False)

    usuario = relationship("Usuario", back_populates="docente")
    unidad = relationship("UnidadAcademica", back_populates="docentes")
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base

class SecretarioAcademico(Base):
    __tablename__ = "secretario_academico"

    id_secretaria = Column(Integer, primary_key=True, autoincrement=True)
    nombre_secretario = Column(String(100), nullable=False)
    id_unidad = Column(Integer, ForeignKey("unidad_academica.id_unidad"), nullable=False)

    unidad = relationship("UnidadAcademica", back_populates="secretarios")
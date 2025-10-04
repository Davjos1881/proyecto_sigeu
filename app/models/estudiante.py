from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base

class Estudiante(Base):
    __tablename__ = "estudiante"

    id_estudiante = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False, unique=True)
    id_programa = Column(Integer, ForeignKey("programa.id_programa"), nullable=False)

    usuario = relationship("Usuario", back_populates="estudiante")
    programa = relationship("Programa")
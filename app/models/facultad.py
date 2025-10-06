from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.mysql import Base
from app.models.programa import Programa

class Facultad(Base):
    __tablename__ = "facultad"

    id_facultad = Column(Integer, primary_key=True, autoincrement=True)
    nombre_facultad = Column(String(100), nullable=False)

    unidades = relationship("UnidadAcademica", back_populates="facultad")
    programas = relationship("Programa", back_populates="facultad")
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.mysql import Base

class Instalacion(Base):
    __tablename__ = "instalacion"

    id_instalacion = Column(Integer, primary_key=True, autoincrement=True)
    nombre_instalacion = Column(String(100), nullable=False)
    ubicacion = Column(String(200), nullable=True)
    tipo_instalacion = Column(String(100), nullable=True)

    eventos = relationship("Evento", back_populates="instalacion")
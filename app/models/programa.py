from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base

class Programa(Base):
    __tablename__ = "programa"

    id_programa = Column(Integer, primary_key=True, autoincrement=True)
    nombre_programa = Column(String(100), nullable=False)
    id_facultad = Column(Integer, ForeignKey("facultad.id_facultad"), nullable=False)

    facultad = relationship("Facultad", back_populates="programas")
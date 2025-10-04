from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.mysql import Base 

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    rol_usuario = Column(String(50), nullable=False)  
    telefono = Column(String(20), nullable=True)

    estudiante = relationship("Estudiante", back_populates="usuario", uselist=False)
    docente = relationship("Docente", back_populates="usuario", uselist=False)
    notificaciones = relationship("Notificacion", back_populates="usuario")
"""
CREATE TABLE paciente (
  idPaciente int NOT NULL,
  nombre varchar(50) NOT NULL,
  fecha_nacimiento date NOT NULL,
  PRIMARY KEY (idPaciente)
);
"""
from app.db.mysql import Base
from sqlalchemy import Integer, Column, String, Date
from sqlalchemy.orm import relationship

class PacienteModel(Base):
    __tablename__ = "paciente"
    idPaciente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)

    #relacion one to many, un paciente a contactos de emergencia
    contactos_emergencia = relationship(
        "ContactoEmergenciaModel", back_populates="paciente",
        cascade="all, delete-orphan"
    )
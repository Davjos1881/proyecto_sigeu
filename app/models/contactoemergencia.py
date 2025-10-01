'''
CREATE TABLE contactosemergencia (
  idContacto int NOT NULL AUTO_INCREMENT,
  nombre varchar(50) NOT NULL,
  relacion varchar(10) DEFAULT NULL,
  pacienteId int DEFAULT NULL,
  PRIMARY KEY (idContacto),
  KEY fk_Paciente_idPaciente_to_ContactosEmergencia_pacienteId (pacienteId),
  CONSTRAINT fk_Paciente_idPaciente_to_ContactosEmergencia_pacienteId FOREIGN KEY (pacienteId) REFERENCES paciente (idPaciente)
);
'''
from app.db.mysql import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Integer, Column, String, Date
from enum import Enum

class ContactoEmergenciaModel(Base):
    __tablename__ = "contactosemergencia"
    idContacto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    relacion = Column(String(50))

    pacienteId = Column(Integer, ForeignKey("paciente.idPaciente"))
    #Relacion Many to one de contacto a paciente
    paciente = relationship("PacienteModel", back_populates="contactos_emergencia")

class RelacionEnum(str, Enum):
    PADRE = "padre"
    MADRE = "madre"
    HERMANO = "hermano"
    ACUDIENTE = "acudiente"
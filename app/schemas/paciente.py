from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.schemas.contactoemergencia import ContactoEmergencia, ContactoEmergenciaCrear

class PacienteBase(BaseModel):
    nombre: str = Field(...,min_length=1, max_length=50)
    fecha_nacimiento: date = Field(
        ..., 
        description="Fecha de nacimiento del paciente",
        examples=["1990-05-15"],
        json_schema_extra={"example": "1990-05-15"}
    )
    
    @field_validator('fecha_nacimiento')
    @classmethod
    def validar_fecha_nacimiento(cls, v):
        """Valida que la fecha de nacimiento no sea futura."""
        if v > date.today():
            raise ValueError('La fecha de nacimiento no puede ser futura')
        return v
    
class PacienteCrear(PacienteBase):
    idPaciente: int  # 🔹 Obligatorio si no es autoincremental
    # Al crear un paciente, también podemos crear sus contactos
    contactos_emergencia: Optional[List[ContactoEmergenciaCrear]] = []

class Paciente(PacienteBase):
    id: int = Field(..., alias="idPaciente")
    contactos_emergencia: List[ContactoEmergencia] = []

    model_config = ConfigDict(from_attributes=True) # ¡Muy importante!

class PacienteActualizar(BaseModel):
    nombre: Optional[str] = None
    fecha_nacimiento: Optional[date] = None


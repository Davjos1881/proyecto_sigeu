from pydantic import BaseModel, ConfigDict,Field
from app.models.contactoemergencia import RelacionEnum

class ContactoEmergenciaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    relacion: RelacionEnum = Field(..., description="Relación con el paciente")

class ContactoEmergenciaCrear(ContactoEmergenciaBase):
   pass

class ContactoEmergencia(ContactoEmergenciaBase):
    id: int = Field(..., alias="idContacto")  # <-- Mapea el nombre real del modelo

    model_config = ConfigDict(from_attributes=True)
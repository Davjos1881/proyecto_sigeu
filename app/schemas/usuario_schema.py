from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from typing import Optional, Literal

ROL_VALUES = ("docente", "estudiante", "secretario")

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    correo: EmailStr
    rol_usuario: str = Field(..., min_length=1, max_length=50)
    telefono: Optional[str] = Field(None, max_length=20)

    @field_validator("rol_usuario")
    @classmethod
    def validar_rol(cls, v: str):
        if v not in ROL_VALUES:
            raise ValueError(f"rol_usuario debe ser uno de {ROL_VALUES}")
        return v

class UsuarioCrear(UsuarioBase):
    pass

class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    rol_usuario: Optional[str] = None
    telefono: Optional[str] = None
    revision_id_revision: Optional[int] = None
    model_config = {"extra": "ignore"}

class UsuarioRead(UsuarioBase):
    id_usuario: int
    nombre: str
    correo: EmailStr
    rol_usuario: str   
    telefono: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    rol_usuario: Optional[str] = None
    telefono: Optional[str] = None
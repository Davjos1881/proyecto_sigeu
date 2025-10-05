from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import evento as crud_evento

ROLES_VALIDOS = ["docente", "estudiante", "administrativo", "externo"]
ROLES_REQUIEREN_AVAL = ["estudiante", "externo"]

def validar_fechas_evento(fecha_inicio: datetime, fecha_fin: datetime):
    if fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin."
        )

async def validar_disponibilidad_instalacion(
    db: AsyncSession, instalacion_id: int, fecha_inicio: datetime, fecha_fin: datetime
):
    solapado = await crud_evento.existe_evento_solapado(
        db, instalacion_id, fecha_inicio, fecha_fin
    )
    if solapado:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La instalación ya está ocupada en esas fechas."
        )

def validar_aval_por_rol(rol: str) -> bool:
    if rol not in ROLES_VALIDOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol de organizador no reconocido."
        )
    return rol in ROLES_REQUIEREN_AVAL

async def validar_evento_completo(
    db: AsyncSession,
    fecha_inicio: datetime,
    fecha_fin: datetime,
    instalacion_id: int,
    rol: str
) -> bool:
    validar_fechas_evento(fecha_inicio, fecha_fin)
    await validar_disponibilidad_instalacion(db, instalacion_id, fecha_inicio, fecha_fin)
    return validar_aval_por_rol(rol)

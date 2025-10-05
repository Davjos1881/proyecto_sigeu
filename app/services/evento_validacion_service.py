from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import evento as crud_evento
from app.crud import acta as crud_acta
from app.crud import notificacion as crud_notificacion


#Constantes de roles

ROLES_VALIDOS = ["docente", "estudiante", "administrativo", "externo"]
ROLES_REQUIEREN_AVAL = ["estudiante", "externo"]


#Validar fechas de evento

def validar_fechas_evento(fecha_inicio: datetime, fecha_fin: datetime):
    if fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin."
        )


#Validar disponibilidad de instalación (no solapamientos)

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


#Reglas de aval según rol del organizador

def validar_aval_por_rol(rol: str) -> bool:
    if rol not in ROLES_VALIDOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol de organizador no reconocido."
        )
    return rol in ROLES_REQUIEREN_AVAL


#Validación completa de evento (antes del CRUD)

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


#Crear notificación interna

async def crear_notificacion_interna(
    db: AsyncSession, tipo: str, mensaje: str, destino: str, evento_id: int = None
):
    await crud_notificacion.crear_notificacion(
        db,
        tipo=tipo,
        mensaje=mensaje,
        destino=destino,
        evento_id=evento_id
    )


#Flujo de revisión de secretaría

async def procesar_revision_secretaria(
    db: AsyncSession, evento_id: int, aprobado: bool, observacion: str
):
    try:
        async with db.begin():  # Transacción atómica
            nuevo_estado = "Aprobado" if aprobado else "Rechazado"

            #Actualizar evento
            await crud_evento.actualizar_estado(db, evento_id, nuevo_estado)

            #Crear acta
            await crud_acta.crear_acta(
                db,
                evento_id=evento_id,
                observacion=observacion,
                estado=nuevo_estado
            )

            #Crear notificación
            mensaje = f"Tu evento ha sido {nuevo_estado.lower()} por Secretaría."
            await crear_notificacion_interna(
                db,
                tipo="revisión_evento",
                mensaje=mensaje,
                destino="organizador",
                evento_id=evento_id
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la revisión: {str(e)}"
        )

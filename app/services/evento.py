from fastapi import HTTPException, status
from datetime import datetime
from app.crud import evento as crud_evento
from app.crud import evento as crud_evento, acta as crud_acta, notificacion as crud_notificacion
from app.models.notificacion import Notificacion


def validar_fechas_evento(fecha_inicio: datetime, fecha_fin: datetime):
    if fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin."
        )


async def validar_disponibilidad_instalacion(db, instalacion_id: int, fecha_inicio: datetime, fecha_fin: datetime):
    solapado = await crud_evento.existe_evento_solapado(db, instalacion_id, fecha_inicio, fecha_fin)
    if solapado:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La instalación ya está ocupada en esas fechas."
        )


def validar_aval_por_rol(rol: str):
    # Definimos qué roles necesitan aval
    roles_requieren_aval = ["estudiante", "externo"]

    if rol not in ["docente", "estudiante", "administrativo", "externo"]:
        raise HTTPException(status_code=400, detail="Rol no reconocido.")

    return rol in roles_requieren_aval


async def procesar_revision_secretaria(db, evento_id: int, aprobado: bool, observacion: str):
    try:
        async with db.begin():  # Transacción atómica
            nuevo_estado = "Aprobado" if aprobado else "Rechazado"

            # 1. Actualizar el estado del evento
            await crud_evento.actualizar_estado(db, evento_id, nuevo_estado)

            # 2. Crear acta
            await crud_acta.crear_acta(db, evento_id=evento_id, observacion=observacion, estado=nuevo_estado)

            # 3. Crear notificación interna
            mensaje = f"Tu evento ha sido {nuevo_estado.lower()} por Secretaría."
            await crud_notificacion.crear_notificacion(
                db,
                tipo="revisión_evento",
                mensaje=mensaje,
                destino="organizador"
            )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en revisión: {str(e)}")


async def crear_notificacion_interna(db, tipo: str, mensaje: str, destino: str):
    notificacion = Notificacion(
        tipo=tipo,
        mensaje=mensaje,
        destino=destino
    )
    db.add(notificacion)
    await db.commit()
    await db.refresh(notificacion)
    return notificacion

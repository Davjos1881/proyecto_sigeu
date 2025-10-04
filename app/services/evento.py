# app/services/evento_service.py

from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import evento as crud_evento
from app.crud import acta as crud_acta
from app.crud import notificacion as crud_notificacion


# ============================================================
# 🧩 Validar fechas de evento
# ============================================================
def validar_fechas_evento(fecha_inicio: datetime, fecha_fin: datetime):
    """
    Verifica que la fecha de inicio no sea posterior a la fecha de fin.
    """
    if fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin."
        )


# ============================================================
# 🧩 Validar disponibilidad de instalación (no solapamientos)
# ============================================================
async def validar_disponibilidad_instalacion(
    db: AsyncSession, instalacion_id: int, fecha_inicio: datetime, fecha_fin: datetime
):
    """
    Verifica que no existan eventos que se solapen con las fechas indicadas
    en la misma instalación.
    """
    solapado = await crud_evento.existe_evento_solapado(
        db, instalacion_id, fecha_inicio, fecha_fin
    )

    if solapado:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La instalación ya está ocupada en esas fechas."
        )


# ============================================================
# 🧩 Reglas de aval según rol del organizador
# ============================================================
def validar_aval_por_rol(rol: str) -> bool:
    """
    Determina si un rol requiere aval adicional.
    """
    roles_requieren_aval = ["estudiante", "externo"]

    if rol not in ["docente", "estudiante", "administrativo", "externo"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol de organizador no reconocido."
        )

    return rol in roles_requieren_aval


# ============================================================
# 🧩 Crear notificación interna
# ============================================================
async def crear_notificacion_interna(
    db: AsyncSession, tipo: str, mensaje: str, destino: str
):
    """
    Genera una notificación interna (solo se guarda en base de datos).
    """
    await crud_notificacion.crear_notificacion(db, tipo, mensaje, destino)


# ============================================================
# 🧩 Flujo de revisión de secretaría
# ============================================================
async def procesar_revision_secretaria(
    db: AsyncSession, evento_id: int, aprobado: bool, observacion: str
):
    """
    Si secretaría aprueba/rechaza un evento:
      - Se actualiza el estado del evento.
      - Se crea el acta correspondiente.
      - Se genera una notificación interna.
    Todo dentro de una transacción atómica.
    """
    try:
        async with db.begin():  # Transacción atómica
            nuevo_estado = "Aprobado" if aprobado else "Rechazado"

            # 1️⃣ Actualizar evento
            await crud_evento.actualizar_estado(db, evento_id, nuevo_estado)

            # 2️⃣ Crear acta
            await crud_acta.crear_acta(
                db,
                evento_id=evento_id,
                observacion=observacion,
                estado=nuevo_estado
            )

            # 3️⃣ Crear notificación
            mensaje = f"Tu evento ha sido {nuevo_estado.lower()} por Secretaría."
            await crud_notificacion.crear_notificacion(
                db,
                tipo="revisión_evento",
                mensaje=mensaje,
                destino="organizador"
            )

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la revisión: {str(e)}"
        )

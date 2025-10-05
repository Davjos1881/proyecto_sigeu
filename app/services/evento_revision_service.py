from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import evento as crud_evento
from app.crud import acta as crud_acta
from app.services.notificacion_service import crear_notificacion_interna

async def procesar_revision_secretaria(
    db: AsyncSession, evento_id: int, aprobado: bool, observacion: str
):
    try:
        async with db.begin():
            nuevo_estado = "Aprobado" if aprobado else "Rechazado"

            await crud_evento.actualizar_estado(db, evento_id, nuevo_estado)

            await crud_acta.crear_acta(
                db,
                evento_id=evento_id,
                observacion=observacion,
                estado=nuevo_estado
            )

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

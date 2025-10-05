from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import notificacion as crud_notificacion

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

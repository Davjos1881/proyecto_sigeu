from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.mysql import get_db
from app.schemas.evento import EventoCreate
from app.services.evento_service import (
    validar_fechas_evento,
    validar_disponibilidad_instalacion,
)
from app.crud import evento as crud_evento

router = APIRouter()

@router.post("/eventos/")
async def crear_evento(evento: EventoCreate, db: AsyncSession = Depends(get_db)):
    # 1️⃣ Validar reglas
    validar_fechas_evento(evento.fecha_inicio, evento.fecha_fin)
    await validar_disponibilidad_instalacion(
        db, evento.instalacion_id, evento.fecha_inicio, evento.fecha_fin
    )

    # 2️⃣ Crear evento si todo está correcto
    nuevo_evento = await crud_evento.crear_evento(db, evento)
    return nuevo_evento

from typing import Optional, Sequence, Dict, Any
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.orm import selectinload
from app.models.evento import EventoModel
from app.schemas.evento_schema import EventoCrear, EventoActualizar

async def crear_evento(session: AsyncSession, evento_in: EventoCrear) -> EventoModel:
    payload = evento_in.model_dump()
    evt_db = EventoModel(**payload)
    # si schema trae relaciones (ej. id_certificado_participacion o listas) añádelas antes del commit
    session.add(evt_db)
    await session.commit()
    await session.refresh(evt_db)
    return evt_db

async def buscar_evento_por_id(session: AsyncSession, id_evento: int) -> Optional[EventoModel]:
    stmt = select(EventoModel).options(selectinload(EventoModel.id_instalacion)).where(EventoModel.id_evento == id_evento)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_eventos(session: AsyncSession, filters: Optional[Dict[str, Any]] = None, limit: int = 50, offset: int = 0) -> Sequence[EventoModel]:
    filters = filters or {}
    stmt = select(EventoModel).order_by(EventoModel.fecha_creacion.desc()).offset(offset).limit(limit)
    if "id_instalacion" in filters:
        stmt = stmt.where(EventoModel.id_instalacion == filters["id_instalacion"])
    if "id_organizacion" in filters:
        stmt = stmt.where(EventoModel.id_organizacion == filters["id_organizacion"])
    if "publicado" in filters:
        stmt = stmt.where(EventoModel.publicado == filters["publicado"])
    if "fecha_inicio_from" in filters:
        stmt = stmt.where(EventoModel.fecha_inicio >= filters["fecha_inicio_from"])
    if "fecha_fin_to" in filters:
        stmt = stmt.where(EventoModel.fecha_fin <= filters["fecha_fin_to"])
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_evento(session: AsyncSession, id_evento: int, update_in: EventoActualizar) -> Optional[EventoModel]:
    evt = await buscar_evento_por_id(session, id_evento)
    if not evt:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(evt, k):
            setattr(evt, k, v)
    session.add(evt)
    await session.commit()
    await session.refresh(evt)
    return evt

async def eliminar_evento(session: AsyncSession, id_evento: int) -> bool:
    evt = await buscar_evento_por_id(session, id_evento)
    if not evt:
        return False
    await session.delete(evt)
    await session.commit()
    return True

async def check_instalacion_disponible(
    session: AsyncSession,
    id_instalacion: int,
    fecha_inicio: date,
    fecha_fin: date,
    exclude_event_id: Optional[int] = None
) -> bool:
    stmt = select(EventoModel).where(EventoModel.id_instalacion == id_instalacion)
    if exclude_event_id:
        stmt = stmt.where(EventoModel.id_evento != exclude_event_id)
    stmt = stmt.where(
        and_(
            EventoModel.fecha_inicio != None,
            EventoModel.fecha_fin != None,
            EventoModel.fecha_inicio <= fecha_fin,
            EventoModel.fecha_fin >= fecha_inicio
        )
    )
    res = await session.execute(stmt)
    conflict = res.scalar_one_or_none()
    return conflict is None
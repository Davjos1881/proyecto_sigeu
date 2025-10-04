from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.aval import AvalEvento as AvalEventoModel
from app.schemas.aval_schema import AvalCrear, AvalRead as AvalEventoCrear, AvalEventoActualizar

async def crear_aval(session: AsyncSession, aval_in: AvalEventoCrear) -> AvalEventoModel:
    payload = aval_in.model_dump()
    aval_db = AvalEventoModel(**payload)
    session.add(aval_db)
    await session.commit()
    await session.refresh(aval_db)
    return aval_db

async def buscar_aval_por_id(session: AsyncSession, id_aval: int) -> Optional[AvalEventoModel]:
    stmt = select(AvalEventoModel).options(selectinload(AvalEventoModel.evento)).where(AvalEventoModel.id_aval == id_aval)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_avales_por_evento(session: AsyncSession, id_evento: int) -> Sequence[AvalEventoModel]:
    stmt = select(AvalEventoModel).where(AvalEventoModel.evento_id_evento == id_evento)
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_aval(session: AsyncSession, id_aval: int, update_in: AvalEventoActualizar) -> Optional[AvalEventoModel]:
    aval = await buscar_aval_por_id(session, id_aval)
    if not aval:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(aval, k):
            setattr(aval, k, v)
    session.add(aval)
    await session.commit()
    await session.refresh(aval)
    return aval

async def eliminar_aval(session: AsyncSession, id_aval: int) -> bool:
    aval = await buscar_aval_por_id(session, id_aval)
    if not aval:
        return False
    await session.delete(aval)
    await session.commit()
    return True
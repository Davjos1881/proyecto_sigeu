from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.programa import Programa as ProgramaModel
from app.schemas.programa_schema import ProgramaCrear, ProgramaActualizar

async def crear_programa(session: AsyncSession, p_in: ProgramaCrear) -> ProgramaModel:
    p_db = ProgramaModel(**p_in.model_dump())
    session.add(p_db)
    await session.commit()
    await session.refresh(p_db)
    return p_db

async def buscar_programa_por_id(session: AsyncSession, id_programa: int) -> Optional[ProgramaModel]:
    stmt = select(ProgramaModel).options(selectinload(ProgramaModel.facultad)).where(ProgramaModel.id_programa == id_programa)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_programas(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[ProgramaModel]:
    stmt = select(ProgramaModel).order_by(ProgramaModel.nombre_programa).offset(offset).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_programa(session: AsyncSession, id_programa: int, update_in: ProgramaActualizar) -> Optional[ProgramaModel]:
    p = await buscar_programa_por_id(session, id_programa)
    if not p:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(p, k):
            setattr(p, k, v)
    session.add(p)
    await session.commit()
    await session.refresh(p)
    return p

async def eliminar_programa(session: AsyncSession, id_programa: int) -> bool:
    p = await buscar_programa_por_id(session, id_programa)
    if not p:
        return False
    await session.delete(p)
    await session.commit()
    return True
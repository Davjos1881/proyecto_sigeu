from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.facultad import Facultad as FacultadModel
from app.schemas.facultad_schema import FacultadCrear, FacultadActualizar

async def crear_facultad(session: AsyncSession, fac_in: FacultadCrear) -> FacultadModel:
    fac_db = FacultadModel(**fac_in.model_dump())
    session.add(fac_db)
    await session.commit()
    await session.refresh(fac_db)
    return fac_db

async def buscar_facultad_por_id(session: AsyncSession, id_facultad: int) -> Optional[FacultadModel]:
    stmt = select(FacultadModel).where(FacultadModel.id_facultad == id_facultad)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_facultades(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[FacultadModel]:
    stmt = select(FacultadModel).order_by(FacultadModel.nombre_facultad).offset(offset).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_facultad(session: AsyncSession, id_facultad: int, update_in: FacultadActualizar) -> Optional[FacultadModel]:
    f = await buscar_facultad_por_id(session, id_facultad)
    if not f:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(f, k):
            setattr(f, k, v)
    session.add(f)
    await session.commit()
    await session.refresh(f)
    return f

async def eliminar_facultad(session: AsyncSession, id_facultad: int) -> bool:
    f = await buscar_facultad_por_id(session, id_facultad)
    if not f:
        return False
    await session.delete(f)
    await session.commit()
    return True
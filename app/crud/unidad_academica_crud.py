from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.unidad_academica import UnidadAcademica as UnidadAcademicaModel
from app.schemas.unidad_academica_schema import UnidadAcademicaCrear, UnidadAcademicaActualizar

async def crear_unidad(session: AsyncSession, unidad_in: UnidadAcademicaCrear) -> UnidadAcademicaModel:
    unidad_db = UnidadAcademicaModel(**unidad_in.model_dump())
    session.add(unidad_db)
    await session.commit()
    await session.refresh(unidad_db)
    return unidad_db

async def buscar_unidad_por_id(session: AsyncSession, id_unidad: int) -> Optional[UnidadAcademicaModel]:
    stmt = select(UnidadAcademicaModel).options(selectinload(UnidadAcademicaModel.facultad)).where(UnidadAcademicaModel.id_unidad == id_unidad)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_unidades(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[UnidadAcademicaModel]:
    stmt = select(UnidadAcademicaModel).order_by(UnidadAcademicaModel.nombre_unidad).offset(offset).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_unidad(session: AsyncSession, id_unidad: int, update_in: UnidadAcademicaActualizar) -> Optional[UnidadAcademicaModel]:
    u = await buscar_unidad_por_id(session, id_unidad)
    if not u:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(u, k):
            setattr(u, k, v)
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u

async def eliminar_unidad(session: AsyncSession, id_unidad: int) -> bool:
    u = await buscar_unidad_por_id(session, id_unidad)
    if not u:
        return False
    await session.delete(u)
    await session.commit()
    return True
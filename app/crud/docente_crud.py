from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.docente import Docente as DocenteModel
from app.schemas.docente_schema import DocenteCrear, DocenteActualizar

async def crear_docente(session: AsyncSession, d_in: DocenteCrear) -> DocenteModel:
    d_db = DocenteModel(**d_in.model_dump())
    session.add(d_db)
    await session.commit()
    await session.refresh(d_db)
    return d_db

async def buscar_docente_por_id(session: AsyncSession, id_docente: int) -> Optional[DocenteModel]:
    stmt = select(DocenteModel).where(DocenteModel.id_docente == id_docente)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_docentes(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[DocenteModel]:
    stmt = select(DocenteModel).order_by(DocenteModel.id_docente).offset(offset).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_docente(session: AsyncSession, id_docente: int, update_in: DocenteActualizar) -> Optional[DocenteModel]:
    d = await buscar_docente_por_id(session, id_docente)
    if not d:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(d, k):
            setattr(d, k, v)
    session.add(d)
    await session.commit()
    await session.refresh(d)
    return d

async def eliminar_docente(session: AsyncSession, id_docente: int) -> bool:
    d = await buscar_docente_por_id(session, id_docente)
    if not d:
        return False
    await session.delete(d)
    await session.commit()
    return True
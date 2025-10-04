from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.revision import Revision as RevisionModel
from app.schemas.revision_schema import RevisionCrear, RevisionActualizar

async def crear_revision(session: AsyncSession, rev_in: RevisionCrear) -> RevisionModel:
    rev_db = RevisionModel(**rev_in.model_dump())
    session.add(rev_db)
    await session.commit()
    await session.refresh(rev_db)
    return rev_db

async def buscar_revision_por_id(session: AsyncSession, id_revision: int) -> Optional[RevisionModel]:
    stmt = select(RevisionModel).where(RevisionModel.id_revision == id_revision)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_revisiones_por_evento(session: AsyncSession, id_evento: int, limit: int = 50, offset: int = 0) -> Sequence[RevisionModel]:
    stmt = select(RevisionModel).where(RevisionModel.id_evento == id_evento).order_by(RevisionModel.fecha_revision.desc()).offset(offset).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_revision(session: AsyncSession, id_revision: int, update_in: RevisionActualizar) -> Optional[RevisionModel]:
    r = await buscar_revision_por_id(session, id_revision)
    if not r:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(r, k):
            setattr(r, k, v)
    session.add(r)
    await session.commit()
    await session.refresh(r)
    return r

async def eliminar_revision(session: AsyncSession, id_revision: int) -> bool:
    r = await buscar_revision_por_id(session, id_revision)
    if not r:
        return False
    await session.delete(r)
    await session.commit()
    return True
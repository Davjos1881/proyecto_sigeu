from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.estudiante import Estudiante as EstudianteModel
from app.schemas.estudiante_schema import EstudianteCrear, EstudianteActualizar

async def crear_estudiante(session: AsyncSession, e_in: EstudianteCrear) -> EstudianteModel:
    e_db = EstudianteModel(**e_in.model_dump())
    session.add(e_db)
    await session.commit()
    await session.refresh(e_db)
    return e_db

async def buscar_estudiante_por_id(session: AsyncSession, id_estudiante: int) -> Optional[EstudianteModel]:
    stmt = select(EstudianteModel).where(EstudianteModel.id_estudiante == id_estudiante)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_estudiantes(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[EstudianteModel]:
    stmt = select(EstudianteModel).order_by(EstudianteModel.id_estudiante).offset(offset).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_estudiante(session: AsyncSession, id_estudiante: int, update_in: EstudianteActualizar) -> Optional[EstudianteModel]:
    e = await buscar_estudiante_por_id(session, id_estudiante)
    if not e:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(e, k):
            setattr(e, k, v)
    session.add(e)
    await session.commit()
    await session.refresh(e)
    return e

async def eliminar_estudiante(session: AsyncSession, id_estudiante: int) -> bool:
    e = await buscar_estudiante_por_id(session, id_estudiante)
    if not e:
        return False
    await session.delete(e)
    await session.commit()
    return True
from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.secretario_academico import SecretarioAcademico as SecretarioAcademicoModel
from app.schemas.secretario_academico_schema import SecretarioCrear, SecretarioActualizar

async def crear_secretario(session: AsyncSession, s_in: SecretarioCrear) -> SecretarioAcademicoModel:
    s_db = SecretarioAcademicoModel(**s_in.model_dump())
    session.add(s_db)
    await session.commit()
    await session.refresh(s_db)
    return s_db

async def buscar_secretario_por_id(session: AsyncSession, id_secretaria: int) -> Optional[SecretarioAcademicoModel]:
    stmt = select(SecretarioAcademicoModel).where(SecretarioAcademicoModel.id_secretaria == id_secretaria)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_secretarios(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[SecretarioAcademicoModel]:
    stmt = select(SecretarioAcademicoModel).order_by(SecretarioAcademicoModel.nombre_secretario).offset(offset).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_secretario(session: AsyncSession, id_secretaria: int, update_in: SecretarioActualizar) -> Optional[SecretarioAcademicoModel]:
    s = await buscar_secretario_por_id(session, id_secretaria)
    if not s:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(s, k):
            setattr(s, k, v)
    session.add(s)
    await session.commit()
    await session.refresh(s)
    return s

async def eliminar_secretario(session: AsyncSession, id_secretaria: int) -> bool:
    s = await buscar_secretario_por_id(session, id_secretaria)
    if not s:
        return False
    await session.delete(s)
    await session.commit()
    return True
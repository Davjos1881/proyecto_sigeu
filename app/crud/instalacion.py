from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.instalacion import InstalacionModel
from app.schemas.instalacion_schema import InstalacionCrear, InstalacionActualizar, InstalacionRead

async def crear_instalacion(session: AsyncSession, instalacion_in: InstalacionCrear) -> InstalacionModel:
    inst_db = InstalacionModel(**instalacion_in.model_dump())
    session.add(inst_db)
    await session.commit()
    await session.refresh(inst_db)
    return inst_db

async def buscar_instalacion_por_id(session: AsyncSession, id_instalacion: int) -> Optional[InstalacionModel]:
    stmt = select(InstalacionModel).where(InstalacionModel.id_instalacion == id_instalacion)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_instalaciones(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[InstalacionModel]:
    stmt = select(InstalacionModel).order_by(InstalacionModel.nombre_instalacion).offset(offset).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_instalacion(session: AsyncSession, id_instalacion: int, update_in: InstalacionActualizar) -> Optional[InstalacionModel]:
    inst = await buscar_instalacion_por_id(session, id_instalacion)
    if not inst:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(inst, k):
            setattr(inst, k, v)
    session.add(inst)
    await session.commit()
    await session.refresh(inst)
    return inst

async def actualizar_instalacion(session: AsyncSession, id_instalacion: int, update_in: InstalacionActualizar) -> Optional[InstalacionRead]:
    stmt = select(InstalacionModel).where(InstalacionModel.id_instalacion == id_instalacion)
    res = await session.execute(stmt)
    inst = res.scalar_one_or_none()
    if not inst:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(inst, k):
            setattr(inst, k, v)
    session.add(inst)
    await session.commit()
    await session.refresh(inst)
    return InstalacionRead.model_validate(inst)

async def eliminar_instalacion(session: AsyncSession, id_instalacion: int) -> bool:
    inst = await buscar_instalacion_por_id(session, id_instalacion)
    if not inst:
        return False
    await session.delete(inst)
    await session.commit()
    return True
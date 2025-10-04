from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.organizacion import OrganizacionExterna as OrganizacionExternaModel
from app.schemas.organizacion_schema import OrganizacionCrear, OrganizacionActualizar, OrganizacionRead

async def crear_organizacion(session: AsyncSession, organizacion_in: OrganizacionCrear) -> OrganizacionExternaModel:
    org_db = OrganizacionExternaModel(**organizacion_in.model_dump())
    session.add(org_db)
    await session.commit()
    await session.refresh(org_db)
    return org_db

async def buscar_organizacion_por_id(session: AsyncSession, id_organizacion: int) -> Optional[OrganizacionExternaModel]:
    stmt = select(OrganizacionExternaModel).where(OrganizacionExternaModel.id_organizacion == id_organizacion)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def buscar_organizacion_por_nombre(session: AsyncSession, nombre: str) -> Optional[OrganizacionExternaModel]:
    stmt = select(OrganizacionExternaModel).where(OrganizacionExternaModel.nombre_organizacion == nombre)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_organizaciones(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[OrganizacionExternaModel]:
    stmt = select(OrganizacionExternaModel).order_by(OrganizacionExternaModel.nombre_organizacion).offset(offset).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_organizacion(session: AsyncSession, id_organizacion: int, update_in: OrganizacionActualizar) -> Optional[OrganizacionRead]:
    stmt = select(OrganizacionExternaModel).where(OrganizacionExternaModel.id_organizacion == id_organizacion)
    res = await session.execute(stmt)
    org = res.scalar_one_or_none()
    if not org:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(org, k):
            setattr(org, k, v)
    session.add(org)
    await session.commit()
    await session.refresh(org)
    return OrganizacionRead.model_validate(org)

async def actualizar_organizacion(session: AsyncSession, id_organizacion: int, update_in: OrganizacionActualizar) -> Optional[OrganizacionExternaModel]:
    org = await buscar_organizacion_por_id(session, id_organizacion)
    if not org:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(org, k):
            setattr(org, k, v)
    session.add(org)
    await session.commit()
    await session.refresh(org)
    return org

async def eliminar_organizacion(session: AsyncSession, id_organizacion: int) -> bool:
    org = await buscar_organizacion_por_id(session, id_organizacion)
    if not org:
        return False
    await session.delete(org)
    await session.commit()
    return True
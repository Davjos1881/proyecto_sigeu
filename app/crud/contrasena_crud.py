from typing import Optional, Sequence
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.contrasena import contrasena as ContrasenaModel
from app.schemas.contrasena import ContrasenaCrear, ContrasenaActualizar

async def crear_contrasena(session: AsyncSession, c_in: ContrasenaCrear) -> ContrasenaModel:
    payload = c_in.model_dump()
    payload.setdefault("fecha_creacion", date.today())
    payload.setdefault("fecha_ultimo_cambio", date.today())
    c_db = ContrasenaModel(**payload)
    session.add(c_db)
    await session.commit()
    await session.refresh(c_db)
    return c_db

async def buscar_contrasena_por_id(session: AsyncSession, id_contrasena: int) -> Optional[ContrasenaModel]:
    stmt = select(ContrasenaModel).where(ContrasenaModel.id_contrasena == id_contrasena)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_contrasenas_por_usuario(session: AsyncSession, id_usuario: int, limit: int = 50, offset: int = 0) -> Sequence[ContrasenaModel]:
    stmt = select(ContrasenaModel).where(ContrasenaModel.usuario_id_usuario == id_usuario).order_by(ContrasenaModel.fecha_creacion.desc()).offset(offset).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_contrasena(session: AsyncSession, id_contrasena: int, update_in: ContrasenaActualizar) -> Optional[ContrasenaModel]:
    c = await buscar_contrasena_por_id(session, id_contrasena)
    if not c:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(c, k):
            setattr(c, k, v)
    session.add(c)
    await session.commit()
    await session.refresh(c)
    return c

async def eliminar_contrasena(session: AsyncSession, id_contrasena: int) -> bool:
    c = await buscar_contrasena_por_id(session, id_contrasena)
    if not c:
        return False
    await session.delete(c)
    await session.commit()
    return True
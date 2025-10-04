from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.usuario import Usuario as UsuarioModel
from app.schemas.usuario_schema import UsuarioCrear, UsuarioActualizar

async def crear_usuario(session: AsyncSession, usuario_in: UsuarioCrear) -> UsuarioModel:
    usuario_db = UsuarioModel(**usuario_in.model_dump())
    session.add(usuario_db)
    await session.commit()
    await session.refresh(usuario_db)
    return usuario_db

async def buscar_usuario_por_id(session: AsyncSession, id_usuario: int) -> Optional[UsuarioModel]:
    stmt = select(UsuarioModel).options(selectinload(UsuarioModel.eventos)).where(UsuarioModel.id_usuario == id_usuario)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def buscar_usuario_por_correo(session: AsyncSession, correo: str) -> Optional[UsuarioModel]:
    stmt = select(UsuarioModel).where(UsuarioModel.correo == correo)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_usuarios(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[UsuarioModel]:
    stmt = select(UsuarioModel).order_by(UsuarioModel.id_usuario).offset(offset).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().unique().all()

async def actualizar_usuario(session: AsyncSession, id_usuario: int, update_in: UsuarioActualizar) -> Optional[UsuarioModel]:
    u = await buscar_usuario_por_id(session, id_usuario)
    if not u:
        return None
    for k, v in update_in.model_dump(exclude_unset=True).items():
        if hasattr(u, k):
            setattr(u, k, v)
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u

async def eliminar_usuario(session: AsyncSession, id_usuario: int) -> bool:
    u = await buscar_usuario_por_id(session, id_usuario)
    if not u:
        return False
    await session.delete(u)
    await session.commit()
    return True
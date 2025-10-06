from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.mysql import get_session
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCrear, UsuarioActualizar, UsuarioRead

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioRead])
async def listar_usuarios(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Usuario))
    usuarios = result.scalars().all()
    return usuarios


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioCrear, db: AsyncSession = Depends(get_session)):
    nuevo = Usuario(**usuario.dict())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


@router.get("/{id_usuario}", response_model=UsuarioRead)
async def obtener_usuario(id_usuario: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Usuario).where(Usuario.id_usuario == id_usuario))
    u = result.scalars().first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return u


@router.put("/{id_usuario}", response_model=UsuarioRead)
async def actualizar_usuario(id_usuario: int, datos: UsuarioActualizar, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Usuario).where(Usuario.id_usuario == id_usuario))
    u = result.scalars().first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for k, v in datos.dict(exclude_unset=True).items():
        setattr(u, k, v)
    await db.commit()
    await db.refresh(u)
    return u


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(id_usuario: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Usuario).where(Usuario.id_usuario == id_usuario))
    u = result.scalars().first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    await db.delete(u)
    await db.commit()
    return None
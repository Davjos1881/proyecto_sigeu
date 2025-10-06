from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.mysql import get_session
from app.models.organizacion import OrganizacionExterna
from app.schemas.organizacion_schema import OrganizacionCrear, OrganizacionActualizar, OrganizacionRead


router = APIRouter(prefix="/organizaciones", tags=["Organizaciones"])


@router.get("/", response_model=List[OrganizacionRead])
async def listar_organizaciones(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(OrganizacionExterna))
    return result.scalars().all()


@router.post("/", response_model=OrganizacionRead, status_code=status.HTTP_201_CREATED)
async def crear_organizacion(o: OrganizacionCrear, db: AsyncSession = Depends(get_session)):
    nuevo = OrganizacionExterna(**o.dict())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


@router.get("/{id_organizacion}", response_model=OrganizacionRead)
async def obtener_organizacion(id_organizacion: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(OrganizacionExterna).filter(OrganizacionExterna.id_organizacion == id_organizacion)
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Organización no encontrada")
    return item


@router.put("/{id_organizacion}", response_model=OrganizacionRead)
async def actualizar_organizacion(id_organizacion: int, datos: OrganizacionActualizar, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(OrganizacionExterna).filter(OrganizacionExterna.id_organizacion == id_organizacion)
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Organización no encontrada")

    for k, v in datos.dict(exclude_unset=True).items():
        setattr(item, k, v)

    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{id_organizacion}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_organizacion(id_organizacion: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(OrganizacionExterna).filter(OrganizacionExterna.id_organizacion == id_organizacion)
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Organización no encontrada")

    await db.delete(item)
    await db.commit()
    return None
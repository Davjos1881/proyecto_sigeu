from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.mysql import get_session
from app.models.docente import Docente
from app.schemas.docente_schema import DocenteCrear, DocenteActualizar, DocenteRead

router = APIRouter(prefix="/docentes", tags=["Docentes"])


@router.get("/", response_model=List[DocenteRead])
async def listar_docentes(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Docente))
    docentes = result.scalars().all()
    return docentes


@router.post("/", response_model=DocenteRead, status_code=status.HTTP_201_CREATED)
async def crear_docente(d: DocenteCrear, db: AsyncSession = Depends(get_session)):
    nuevo = Docente(**d.dict())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


@router.get("/{id_docente}", response_model=DocenteRead)
async def obtener_docente(id_docente: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Docente).filter(Docente.id_docente == id_docente))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return item


@router.put("/{id_docente}", response_model=DocenteRead)
async def actualizar_docente(id_docente: int, datos: DocenteActualizar, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Docente).filter(Docente.id_docente == id_docente))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    for k, v in datos.dict(exclude_unset=True).items():
        setattr(item, k, v)

    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{id_docente}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_docente(id_docente: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Docente).filter(Docente.id_docente == id_docente))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    await db.delete(item)
    await db.commit()
    return None
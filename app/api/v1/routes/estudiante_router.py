from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.mysql import get_session 
from app.models.estudiante import Estudiante
from app.schemas.estudiante_schema import EstudianteCrear, EstudianteActualizar, EstudianteRead

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.get("/", response_model=List[EstudianteRead])
async def listar_estudiantes(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Estudiante))
    estudiantes = result.scalars().all()
    return estudiantes


@router.post("/", response_model=EstudianteRead, status_code=status.HTTP_201_CREATED)
async def crear_estudiante(e: EstudianteCrear, db: AsyncSession = Depends(get_session)):
    nuevo = Estudiante(**e.dict())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


@router.get("/{id_estudiante}", response_model=EstudianteRead)
async def obtener_estudiante(id_estudiante: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Estudiante).filter(Estudiante.id_estudiante == id_estudiante))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return item


@router.put("/{id_estudiante}", response_model=EstudianteRead)
async def actualizar_estudiante(id_estudiante: int, datos: EstudianteActualizar, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Estudiante).filter(Estudiante.id_estudiante == id_estudiante))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    for k, v in datos.dict(exclude_unset=True).items():
        setattr(item, k, v)

    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{id_estudiante}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_estudiante(id_estudiante: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Estudiante).filter(Estudiante.id_estudiante == id_estudiante))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    await db.delete(item)
    await db.commit()
    return None
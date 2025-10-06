from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.mysql import get_session
from app.models.aval import AvalEvento
from app.schemas.aval_schema import AvalCrear, AvalEventoActualizar, AvalRead
from typing import List

router = APIRouter(
    prefix="/avales",
    tags=["Avales"]
)

# Crear un aval
@router.post("/", response_model=AvalRead, status_code=status.HTTP_201_CREATED)
async def crear_aval(aval: AvalCrear, db: AsyncSession = Depends(get_session)):
    nuevo_aval = AvalEvento(**aval.dict())
    db.add(nuevo_aval)
    await db.commit()
    await db.refresh(nuevo_aval)
    return nuevo_aval

# Listar avales
@router.get("/", response_model=List[AvalRead])
async def listar_avales(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(AvalEvento))
    avales = result.scalars().all()
    return avales

# Obtener un aval por ID
@router.get("/{id_aval}", response_model=AvalRead)
async def obtener_aval(id_aval: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(AvalEvento).where(AvalEvento.id_aval == id_aval))
    aval = result.scalars().first()
    if not aval:
        raise HTTPException(status_code=404, detail="Aval no encontrado")
    return aval

# Actualizar un aval
@router.put("/{id_aval}", response_model=AvalRead)
async def actualizar_aval(id_aval: int, aval_update: AvalEventoActualizar, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(AvalEvento).where(AvalEvento.id_aval == id_aval))
    aval = result.scalars().first()
    if not aval:
        raise HTTPException(status_code=404, detail="Aval no encontrado")

    for key, value in aval_update.dict(exclude_unset=True).items():
        setattr(aval, key, value)

    await db.commit()
    await db.refresh(aval)
    return aval

# Eliminar un aval
@router.delete("/{id_aval}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_aval(id_aval: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(AvalEvento).where(AvalEvento.id_aval == id_aval))
    aval = result.scalars().first()
    if not aval:
        raise HTTPException(status_code=404, detail="Aval no encontrado")

    await db.delete(aval)
    await db.commit()
    return None
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import date
from typing import List

from app.db.mysql import get_session
from app.models.evento import Evento
from app.schemas.evento_schema import EventoCrear, EventoActualizar, EventoRead

router = APIRouter(prefix="/eventos", tags=["Eventos"])


@router.get("/", response_model=List[EventoRead])
async def listar_eventos(db: AsyncSession = Depends(get_session)):
    stmt = (
        select(Evento)
        .options(
            selectinload(Evento.organizacion),
            selectinload(Evento.instalacion),
            selectinload(Evento.certificado),
            selectinload(Evento.avales),
            selectinload(Evento.revisiones),
            selectinload(Evento.notificaciones),
        )
    )
    result = await db.execute(stmt)
    eventos = result.scalars().unique().all()
    return eventos


@router.get("/{id_evento}", response_model=EventoRead)
async def obtener_evento(id_evento: int, db: AsyncSession = Depends(get_session)):
    stmt = (
        select(Evento)
        .options(
            selectinload(Evento.organizacion),
            selectinload(Evento.instalacion),
            selectinload(Evento.certificado),
            selectinload(Evento.avales),
            selectinload(Evento.revisiones),
            selectinload(Evento.notificaciones),
        )
        .where(Evento.id_evento == id_evento)
    )
    result = await db.execute(stmt)
    evento = result.scalars().first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento


@router.post("/", response_model=EventoRead, status_code=status.HTTP_201_CREATED)
async def crear_evento(evento: EventoCrear, db: AsyncSession = Depends(get_session)):
    nuevo_evento = Evento(**evento.dict())
    nuevo_evento.fecha_creacion = date.today()
    db.add(nuevo_evento)
    await db.commit()
    await db.refresh(nuevo_evento)
    return nuevo_evento


@router.put("/{id_evento}", response_model=EventoRead)
async def actualizar_evento(id_evento: int, datos: EventoActualizar, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Evento).where(Evento.id_evento == id_evento))
    evento = result.scalars().first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(evento, key, value)

    await db.commit()
    await db.refresh(evento)
    return evento


@router.delete("/{id_evento}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_evento(id_evento: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Evento).where(Evento.id_evento == id_evento))
    evento = result.scalars().first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    await db.delete(evento)
    await db.commit()
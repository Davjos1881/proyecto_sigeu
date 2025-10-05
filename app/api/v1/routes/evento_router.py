from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.db.database import get_db
from app.models.evento import Evento
from app.schemas.evento_schema import EventoCrear, EventoActualizar, EventoRead

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.get("/", response_model=List[EventoRead])
def listar_eventos(db: Session = Depends(get_db)):
    return db.query(Evento).all()


@router.post("/", response_model=EventoRead)
def crear_evento(evento: EventoCrear, db: Session = Depends(get_db)):
    nuevo_evento = Evento(**evento.dict())
    nuevo_evento.fecha_creacion = date.today()
    db.add(nuevo_evento)
    db.commit()
    db.refresh(nuevo_evento)
    return nuevo_evento


@router.get("/{id_evento}", response_model=EventoRead)
def obtener_evento(id_evento: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == id_evento).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento



@router.put("/{id_evento}", response_model=EventoRead)
def actualizar_evento(id_evento: int, datos: EventoActualizar, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == id_evento).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(evento, key, value)

    db.commit()
    db.refresh(evento)
    return evento


@router.delete("/{id_evento}")
def eliminar_evento(id_evento: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == id_evento).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    db.delete(evento)
    db.commit()
    return {"mensaje": "Evento eliminado correctamente"}

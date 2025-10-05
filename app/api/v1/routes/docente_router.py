from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.docente import Docente
from app.schemas.docente_schema import DocenteCrear, DocenteActualizar, DocenteRead

router = APIRouter(prefix="/docentes", tags=["Docentes"])


@router.get("/", response_model=List[DocenteRead])
def listar_docentes(db: Session = Depends(get_db)):
    return db.query(Docente).all()


@router.post("/", response_model=DocenteRead, status_code=status.HTTP_201_CREATED)
def crear_docente(d: DocenteCrear, db: Session = Depends(get_db)):
    nuevo = Docente(**d.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/{id_docente}", response_model=DocenteRead)
def obtener_docente(id_docente: int, db: Session = Depends(get_db)):
    item = db.query(Docente).filter(Docente.id_docente == id_docente).first()
    if not item:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return item


@router.put("/{id_docente}", response_model=DocenteRead)
def actualizar_docente(id_docente: int, datos: DocenteActualizar, db: Session = Depends(get_db)):
    item = db.query(Docente).filter(Docente.id_docente == id_docente).first()
    if not item:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    for k, v in datos.dict(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{id_docente}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_docente(id_docente: int, db: Session = Depends(get_db)):
    item = db.query(Docente).filter(Docente.id_docente == id_docente).first()
    if not item:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    db.delete(item)
    db.commit()
    return None

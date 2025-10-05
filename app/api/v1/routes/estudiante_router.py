from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.estudiante import Estudiante
from app.schemas.estudiante_schema import EstudianteCrear, EstudianteActualizar, EstudianteRead

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.get("/", response_model=List[EstudianteRead])
def listar_estudiantes(db: Session = Depends(get_db)):
    return db.query(Estudiante).all()


@router.post("/", response_model=EstudianteRead, status_code=status.HTTP_201_CREATED)
def crear_estudiante(e: EstudianteCrear, db: Session = Depends(get_db)):
    nuevo = Estudiante(**e.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/{id_estudiante}", response_model=EstudianteRead)
def obtener_estudiante(id_estudiante: int, db: Session = Depends(get_db)):
    item = db.query(Estudiante).filter(Estudiante.id_estudiante == id_estudiante).first()
    if not item:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return item


@router.put("/{id_estudiante}", response_model=EstudianteRead)
def actualizar_estudiante(id_estudiante: int, datos: EstudianteActualizar, db: Session = Depends(get_db)):
    item = db.query(Estudiante).filter(Estudiante.id_estudiante == id_estudiante).first()
    if not item:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    for k, v in datos.dict(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{id_estudiante}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiante(id_estudiante: int, db: Session = Depends(get_db)):
    item = db.query(Estudiante).filter(Estudiante.id_estudiante == id_estudiante).first()
    if not item:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    db.delete(item)
    db.commit()
    return None

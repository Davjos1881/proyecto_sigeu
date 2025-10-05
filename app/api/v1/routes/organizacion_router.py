from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.organizacion import OrganizacionExterna
from app.schemas.organizacion_schema import OrganizacionCrear, OrganizacionActualizar, OrganizacionRead

router = APIRouter(prefix="/organizaciones", tags=["Organizaciones"])


@router.get("/", response_model=List[OrganizacionRead])
def listar_organizaciones(db: Session = Depends(get_db)):
    return db.query(OrganizacionExterna).all()


@router.post("/", response_model=OrganizacionRead, status_code=status.HTTP_201_CREATED)
def crear_organizacion(o: OrganizacionCrear, db: Session = Depends(get_db)):
    nuevo = OrganizacionExterna(**o.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/{id_organizacion}", response_model=OrganizacionRead)
def obtener_organizacion(id_organizacion: int, db: Session = Depends(get_db)):
    item = db.query(OrganizacionExterna).filter(OrganizacionExterna.id_organizacion == id_organizacion).first()
    if not item:
        raise HTTPException(status_code=404, detail="Organización no encontrada")
    return item


@router.put("/{id_organizacion}", response_model=OrganizacionRead)
def actualizar_organizacion(id_organizacion: int, datos: OrganizacionActualizar, db: Session = Depends(get_db)):
    item = db.query(OrganizacionExterna).filter(OrganizacionExterna.id_organizacion == id_organizacion).first()
    if not item:
        raise HTTPException(status_code=404, detail="Organización no encontrada")
    for k, v in datos.dict(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{id_organizacion}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_organizacion(id_organizacion: int, db: Session = Depends(get_db)):
    item = db.query(OrganizacionExterna).filter(OrganizacionExterna.id_organizacion == id_organizacion).first()
    if not item:
        raise HTTPException(status_code=404, detail="Organización no encontrada")
    db.delete(item)
    db.commit()
    return None

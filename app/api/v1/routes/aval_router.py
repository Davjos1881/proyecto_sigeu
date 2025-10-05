from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.aval import AvalEvento
from app.schemas.aval_schema import AvalCrear, AvalEventoActualizar, AvalRead
from typing import List

router = APIRouter(
    prefix="/avales",
    tags=["Avales"]
)

# Crear un aval
@router.post("/", response_model=AvalRead, status_code=status.HTTP_201_CREATED)
def crear_aval(aval: AvalCrear, db: Session = Depends(get_db)):
    nuevo_aval = AvalEvento(**aval.dict())
    db.add(nuevo_aval)
    db.commit()
    db.refresh(nuevo_aval)
    return nuevo_aval



@router.get("/", response_model=List[AvalRead])
def listar_avales(db: Session = Depends(get_db)):
    avales = db.query(AvalEvento).all()
    return avales



@router.get("/{id_aval}", response_model=AvalRead)
def obtener_aval(id_aval: int, db: Session = Depends(get_db)):
    aval = db.query(AvalEvento).filter(AvalEvento.id_aval == id_aval).first()
    if not aval:
        raise HTTPException(status_code=404, detail="Aval no encontrado")
    return aval


# Actualizar un aval
@router.put("/{id_aval}", response_model=AvalRead)
def actualizar_aval(id_aval: int, aval_update: AvalEventoActualizar, db: Session = Depends(get_db)):
    aval = db.query(AvalEvento).filter(AvalEvento.id_aval == id_aval).first()
    if not aval:
        raise HTTPException(status_code=404, detail="Aval no encontrado")

    for key, value in aval_update.dict(exclude_unset=True).items():
        setattr(aval, key, value)

    db.commit()
    db.refresh(aval)
    return aval


@router.delete("/{id_aval}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_aval(id_aval: int, db: Session = Depends(get_db)):
    aval = db.query(AvalEvento).filter(AvalEvento.id_aval == id_aval).first()
    if not aval:
        raise HTTPException(status_code=404, detail="Aval no encontrado")

    db.delete(aval)
    db.commit()
    return None


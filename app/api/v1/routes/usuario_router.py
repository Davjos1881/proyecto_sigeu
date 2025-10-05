from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCrear, UsuarioActualizar, UsuarioRead

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioRead])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCrear, db: Session = Depends(get_db)):
    nuevo = Usuario(**usuario.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    u = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return u


@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(id_usuario: int, datos: UsuarioActualizar, db: Session = Depends(get_db)):
    u = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for k, v in datos.dict(exclude_unset=True).items():
        setattr(u, k, v)
    db.commit()
    db.refresh(u)
    return u


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    u = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(u)
    db.commit()
    return None

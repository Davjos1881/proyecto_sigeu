from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.certificado import CertificadoParticipacion
from app.schemas.certificado_schema import CertificadoCrear, CertificadoActualizar, CertificadoRead

router = APIRouter(
    prefix="/certificados",
    tags=["Certificados de Participación"]
)

# Crear un certificado
@router.post("/", response_model=CertificadoRead, status_code=status.HTTP_201_CREATED)
def crear_certificado(cert: CertificadoCrear, db: Session = Depends(get_db)):
    nuevo_cert = CertificadoParticipacion(**cert.dict())
    db.add(nuevo_cert)
    db.commit()
    db.refresh(nuevo_cert)
    return nuevo_cert


# Listar todos los certificados
@router.get("/", response_model=List[CertificadoRead])
def listar_certificados(db: Session = Depends(get_db)):
    certificados = db.query(CertificadoParticipacion).all()
    return certificados


# Obtener un certificado por ID
@router.get("/{id_certificado}", response_model=CertificadoRead)
def obtener_certificado(id_certificado: int, db: Session = Depends(get_db)):
    cert = db.query(CertificadoParticipacion).filter(CertificadoParticipacion.id_certificado == id_certificado).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")
    return cert


# Actualizar un certificado
@router.put("/{id_certificado}", response_model=CertificadoRead)
def actualizar_certificado(id_certificado: int, cert_update: CertificadoActualizar, db: Session = Depends(get_db)):
    cert = db.query(CertificadoParticipacion).filter(CertificadoParticipacion.id_certificado == id_certificado).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")

    for key, value in cert_update.dict(exclude_unset=True).items():
        setattr(cert, key, value)

    db.commit()
    db.refresh(cert)
    return cert


# Eliminar un certificado
@router.delete("/{id_certificado}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_certificado(id_certificado: int, db: Session = Depends(get_db)):
    cert = db.query(CertificadoParticipacion).filter(CertificadoParticipacion.id_certificado == id_certificado).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")

    db.delete(cert)
    db.commit()
    return None

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.mysql import get_session
from app.models.certificado import CertificadoParticipacion
from app.schemas.certificado_schema import CertificadoCrear, CertificadoActualizar, CertificadoRead

router = APIRouter(
    prefix="/certificados",
    tags=["Certificados de Participación"]
)

# Crear un certificado
@router.post("/", response_model=CertificadoRead, status_code=status.HTTP_201_CREATED)
async def crear_certificado(cert: CertificadoCrear, db: AsyncSession = Depends(get_session)):
    nuevo_cert = CertificadoParticipacion(**cert.dict())
    db.add(nuevo_cert)
    await db.commit()
    await db.refresh(nuevo_cert)
    return nuevo_cert


# Listar todos los certificados
@router.get("/", response_model=List[CertificadoRead])
async def listar_certificados(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CertificadoParticipacion))
    certificados = result.scalars().all()
    return certificados


# Obtener un certificado por ID
@router.get("/{id_certificado}", response_model=CertificadoRead)
async def obtener_certificado(id_certificado: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(CertificadoParticipacion).where(CertificadoParticipacion.id_certificado == id_certificado)
    )
    cert = result.scalars().first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")
    return cert


# Actualizar un certificado
@router.put("/{id_certificado}", response_model=CertificadoRead)
async def actualizar_certificado(id_certificado: int, cert_update: CertificadoActualizar, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(CertificadoParticipacion).where(CertificadoParticipacion.id_certificado == id_certificado)
    )
    cert = result.scalars().first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")

    for key, value in cert_update.dict(exclude_unset=True).items():
        setattr(cert, key, value)

    await db.commit()
    await db.refresh(cert)
    return cert


# Eliminar un certificado
@router.delete("/{id_certificado}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_certificado(id_certificado: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(CertificadoParticipacion).where(CertificadoParticipacion.id_certificado == id_certificado)
    )
    cert = result.scalars().first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificado no encontrado")

    await db.delete(cert)
    await db.commit()
    return None
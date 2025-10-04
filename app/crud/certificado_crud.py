from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.certificado import CertificadoParticipacion as CertificadoParticipacionModel
from app.schemas.certificado_schema import CertificadoCrear

async def crear_certificado(session: AsyncSession, cert_in: CertificadoCrear) -> CertificadoParticipacionModel:
    cert_db = CertificadoParticipacionModel(**cert_in.model_dump())
    session.add(cert_db)
    await session.commit()
    await session.refresh(cert_db)
    return cert_db

async def buscar_certificado_por_id(session: AsyncSession, id_certificado: int) -> Optional[CertificadoParticipacionModel]:
    stmt = select(CertificadoParticipacionModel).where(CertificadoParticipacionModel.id_certificado == id_certificado)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def listar_certificados(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[CertificadoParticipacionModel]:
    stmt = select(CertificadoParticipacionModel).order_by(CertificadoParticipacionModel.id_certificado.desc()).offset(offset).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().unique().all()


async def eliminar_certificado(session: AsyncSession, id_certificado: int) -> bool:
    cert = await buscar_certificado_por_id(session, id_certificado)
    if not cert:
        return False
    await session.delete(cert)
    await session.commit()
    return True
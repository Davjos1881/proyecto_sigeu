from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from datetime import date
from sqlalchemy.orm import selectinload
from app.models.paciente import PacienteModel
from app.models.contactoemergencia import ContactoEmergenciaModel
from app.schemas.paciente import PacienteCrear

async def crear_paciente(session: AsyncSession, paciente_in: PacienteCrear) -> PacienteModel:
    # Creamos el objeto Paciente del modelo SQLAlchemy
    paciente_db = PacienteModel(
        idPaciente=paciente_in.idPaciente,
        nombre=paciente_in.nombre,
        fecha_nacimiento=paciente_in.fecha_nacimiento
    )
    # Creamos los objetos de Contacto si existen
    if paciente_in.contactos_emergencia:
        for contacto_in in paciente_in.contactos_emergencia:
            contacto_db = ContactoEmergenciaModel(**contacto_in.model_dump(), paciente=paciente_db)
            session.add(contacto_db)

    session.add(paciente_db)
    await session.commit()
    await session.refresh(paciente_db, ["contactos_emergencia"]) # Refrescar para obtener relaciones
    return paciente_db

async def buscar_paciente_por_nombre_y_fecha(
    session: AsyncSession,
    nombre: str,
    fecha_nacimiento: date
) -> Optional[PacienteModel]:
    """
    Busca un paciente por nombre exacto y fecha de nacimiento.
    Retorna el modelo ORM si lo encuentra, de lo contrario None.
    """
    stmt = select(PacienteModel).where(
        PacienteModel.nombre == nombre,
        PacienteModel.fecha_nacimiento == fecha_nacimiento
    )

    result = await session.execute(stmt)
    paciente = result.scalar_one_or_none()

    return paciente

async def listar_paciente(session: AsyncSession) -> Sequence[PacienteModel]:
    stmt = (select(PacienteModel)

    .options(selectinload(PacienteModel.contactos_emergencia))
    .order_by(PacienteModel.idPaciente)
    )

    result = await session.execute(stmt)
    pacientes = result.scalars().unique().all()

    return pacientes

async def buscar_paciente_por_id(
    session: AsyncSession,
    id_paciente: int
) -> Optional[PacienteModel]:
    stmt = (
        select(PacienteModel)
        .options(selectinload(PacienteModel.contactos_emergencia))).where(PacienteModel.idPaciente == id_paciente)

    result = await session.execute(stmt)
    paciente = result.scalar_one_or_none()
    return paciente
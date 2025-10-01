from typing import Optional
from sqlalchemy.orm import selectinload
from sqlalchemy import Sequence, select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import paciente as paciente_crud
from app.schemas.paciente import PacienteCrear
from app.models.paciente import PacienteModel

# Aquí se podría importar otros módulos, como un servicio de notificaciones

async def crear_paciente_service(session: AsyncSession, nuevo_paciente: PacienteCrear) -> PacienteModel:
    # --- PASO 1: LÓGICA DE NEGOCIO (VALIDACIÓN) ---
    # Regla: No permitir duplicados exactos (mismo nombre y fecha de nacimiento).
    paciente_existente = await paciente_crud.buscar_paciente_por_nombre_y_fecha(
        session,
        nombre=nuevo_paciente.nombre,
        fecha_nacimiento=nuevo_paciente.fecha_nacimiento
    )

    if paciente_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un paciente con el mismo nombre y fecha de nacimiento.",
        )

    try:
        # --- PASO 2: LLAMADA A LA CAPA CRUD ---
        # Si todas las validaciones pasan, le pedimos al CRUD que cree el paciente.
        paciente_creado = await paciente_crud.crear_paciente(session, nuevo_paciente)
        # --- PASO 3: RETORNAR EL RESULTADO ---
        # Devolvemos el modelo del paciente creado.
        return paciente_creado
    except IntegrityError as e:
        # Se deshace la transacción y se lanza el error. FastAPI maneja automáticamente el rollback
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un paciente con el mismo ID (idPaciente)."
        ) from e
    
async def listar_pacientes_service(session: AsyncSession) -> Sequence[PacienteModel]:
    pacientes = await paciente_crud.listar_paciente(session)
    return pacientes

async def buscar_paciente_por_id(
    session: AsyncSession,
    id_paciente: int
) -> PacienteModel:
    paciente = await paciente_crud.buscar_paciente_por_id(session, id_paciente)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No se encontró el paciente con el id {id_paciente}'
        )
    return paciente

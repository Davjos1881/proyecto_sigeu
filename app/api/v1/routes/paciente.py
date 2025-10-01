from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.mysql import get_session
from app.services import paciente as paciente_service
from app.schemas.paciente import PacienteCrear, Paciente

router = APIRouter()

@router.post("/", response_model=Paciente, status_code=status.HTTP_201_CREATED)
async def crear_paciente(
    paciente: PacienteCrear,
    session: AsyncSession = Depends(get_session)
):
    paciente_modelo = await paciente_service.crear_paciente_service(session, paciente)
    return paciente_modelo # Pydantic convierte el modelo SQLAlchemy al schema gracias a from_attributes=True

@router.get("/", response_model=List[Paciente], status_code=status.HTTP_200_OK)
async def listar_pacientes(
    session: AsyncSession = Depends(get_session)
):
    pacientes = await paciente_service.listar_pacientes_service(session)
    return pacientes

@router.get("/{id_paciente}", response_model=Paciente, status_code=status.HTTP_200_OK)
async def obtener_paciente_por_id(
    id_paciente: int,
    session: AsyncSession = Depends(get_session)
):
    paciente = await paciente_service.buscar_paciente_por_id(session, id_paciente)
    return paciente

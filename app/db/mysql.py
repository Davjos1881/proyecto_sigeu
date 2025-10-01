from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Paso 1: Crear el motor asíncrono
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Muestra las consultas SQL en consola si está en modo DEBUG
)

# Paso 2: Crear el sessionmaker SIN bind (para evitar errores de tipado)
AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
)

# Paso 3: Declarative base para modelos ORM
Base = declarative_base()

# Paso 4: Dependencia para FastAPI que retorna una sesión por petición
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependencia de FastAPI para inyectar una sesión de BD por petición.
    """
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        yield session

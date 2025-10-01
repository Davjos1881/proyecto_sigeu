from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    # Configuración de base de datos
    DATABASE_URL: str = Field(
        ..., 
        description="URL de conexión a la base de datos MySQL"
    )
    DEBUG: bool = Field(
        default=False, 
        description="Modo debug para SQLAlchemy (muestra consultas SQL en consola)"
    )
    
    # Configuración de la aplicación
    APP_NAME: str = Field(
        default="API del Sistema SIGEU BDR", 
        description="Nombre de la aplicación"
    )
    APP_VERSION: str = Field(
        default="1.0.0", 
        description="Versión de la aplicación"
    )
    
    # Configuración de CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["*"], 
        description="Orígenes permitidos para CORS"
    )
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() # type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Importa el enrutador principal que agrupa todos los endpoints de la v1
from app.api.v1.api import api_router_v1
# Importa la configuración centralizada
from app.core.config import settings

# Crea la instancia principal de la aplicación FastAPI
# Se añade metadata que se usará en la documentación automática de la API
app = FastAPI(
    title=settings.APP_NAME,
    description="Una API para la creación y gestión de eventos universitarios",
    version=settings.APP_VERSION,
)
# --- Configuración de Middleware CORS ---
# Configura CORS para permitir solicitudes desde orígenes permitidos de un frontend (dominios/puertos) antes de que 
# lleguen a los endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Inclusión de Enrutadores de la API ---

# Incluye todas las rutas de la v1 bajo el prefijo global /api/v1
# La URL final para crear un paciente será: http://.../api/v1/pacientes/
app.include_router(api_router_v1, prefix="/api/v1")

# Redirección automática de la raíz a la documentación
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


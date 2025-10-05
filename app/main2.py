from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi import FastAPI


app = FastAPI(title="SIGEU API")



# Importa el enrutador principal que agrupa todos los endpoints de la v1
from app.api.v1.api import api_router_v1
# Importa la configuración centralizada
from app.core.config import settings

# Importar routers individuales para registrarlos en la aplicación principal
from app.api.v1.routes import (
    evento_router,
    certificado_router,
    aval_router,
    usuario_router,
    estudiante_router,
    docente_router,
    organizacion_router,
)

# Crea la instancia principal de la aplicación FastAPI
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

# Incluir routers individuales bajo el prefijo /api/v1
app.include_router(evento_router.router, prefix="/api/v1")
app.include_router(certificado_router.router, prefix="/api/v1")
app.include_router(aval_router.router, prefix="/api/v1")
app.include_router(usuario_router.router, prefix="/api/v1")
app.include_router(estudiante_router.router, prefix="/api/v1")
app.include_router(docente_router.router, prefix="/api/v1")

app.include_router(organizacion_router.router, prefix="/api/v1")

# Redirección automática de la raíz a la documentación
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


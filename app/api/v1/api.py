from fastapi import APIRouter

# Importa 

# Crea un enrutador principal para la v1
api_router_v1 = APIRouter()

# Incluye el enrutador de pacientes bajo el prefijo /pacientes
# Todas las rutas en paciente.router ahora comenzarán con /pacientes
# y estarán agrupadas bajo la etiqueta "Pacientes" en la documentación.
# Si en el futuro se tiene un enrutador para "Doctores", se deberá aquí:
# from app.api.v1.routes import doctor
# api_router_v1.include_router(doctor.router, prefix="/doctores", tags=["Doctores"])
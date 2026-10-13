from fastapi import FastAPI
<<<<<<< HEAD
from app.api import (
    rutas_perfil, 
    rutas_modulos, 
    rutas_motivos, 
    rutas_acudientes, 
    rutas_estudiantes,
     rutas_primera_clase

)

app = FastAPI(
    title="API - Sistema de Control de Llegadas Tarde",
    description="Backend modular en FastAPI y PostgreSQL para gestión de asistencia escolar",
    version="1.0.0"
)

app.include_router(rutas_perfil.router)
app.include_router(rutas_modulos.router)
app.include_router(rutas_motivos.router)
app.include_router(rutas_acudientes.router)
app.include_router(rutas_estudiantes.router)
app.include_router(rutas_primera_clase.router)


@app.get("/", tags=["default"], summary="Estado de la API")
def estado():
    return {"status": "ok", "mensaje": "API escolar activa y funcional"}
=======
from app.api import rutas_usuario
from app.api import rutas_moduloxrol
from app.api import rutas_estudxacudiente
from app.api import rutas_coordinador
from app.api import rutas_asistenciaxestudiante
from app.api import rutas_registronotificaciones
# Me faltan las demas rutas

app = FastAPI(
    title="API Parcial 1 - Módulo Web",
    description="Backend firme para el proyecto de la universidad",
    version="1.0.0"
)

app.include_router(rutas_usuario.router)
app.include_router(rutas_moduloxrol.router)
app.include_router(rutas_estudxacudiente.router)
app.include_router(rutas_coordinador.router)
app.include_router(rutas_asistenciaxestudiante.router)
app.include_router(rutas_registronotificaciones.router)

@app.get("/")
def estado_api():
    return {"La API está corriendo melo caramelo"}
>>>>>>> 228d19d134f84dfa62c39841e25fd7c0e036e184

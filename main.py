from fastapi import FastAPI
from app.api import (
    rutas_perfil, 
    rutas_modulos, 
    rutas_motivos, 
    rutas_acudientes, 
    rutas_estudiantes,
    rutas_primera_clase,
    rutas_auth,
    rutas_usuario,
    rutas_moduloxrol,
    rutas_estudxacudiente,
    rutas_coordinador,
    rutas_asistenciaxestudiante,
    rutas_registronotificaciones

)

app = FastAPI(
    title="API - Sistema de Control de Llegadas Tarde",
    description="Backend modular en FastAPI y PostgreSQL para gestión de asistencia escolar",
    version="1.0.0"
)

app.include_router(rutas_auth.router)
app.include_router(rutas_perfil.router)
app.include_router(rutas_modulos.router)
app.include_router(rutas_motivos.router)
app.include_router(rutas_acudientes.router)
app.include_router(rutas_estudiantes.router)
app.include_router(rutas_primera_clase.router)
app.include_router(rutas_usuario.router)
app.include_router(rutas_moduloxrol.router)
app.include_router(rutas_estudxacudiente.router)
app.include_router(rutas_coordinador.router)
app.include_router(rutas_asistenciaxestudiante.router)
app.include_router(rutas_registronotificaciones.router)


@app.get("/", tags=["default"], summary="Estado de la API")
def estado():
    return {"status": "ok", "mensaje": "API escolar activa y funcional"}

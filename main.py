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
    rutas_curso,
    rutas_registronotificaciones
)

app = FastAPI(
    title="API de Gestión de llegadas tarde",
    description="Backend modular para monitoreo académico usando FastAPI y PostgreSQL puro",
    version="1.0.0"
)

# Conectamos el módulo de rutas a la aplicación principal
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
app.include_router(rutas_curso.router)
app.include_router(rutas_registronotificaciones.router)

@app.get("/")
def estado_api():
    return {"mensaje": "La API de monitoreo se encuentra en línea y funcional"}
from fastapi import FastAPI
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
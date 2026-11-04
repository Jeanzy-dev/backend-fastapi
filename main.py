from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.rutas_auth import router as router_auth
from app.api.rutas_perfil import router as router_perfiles
from app.api.rutas_modulos import router as router_modulos
from app.api.rutas_moduloxrol import router as router_moduloxrol
from app.api.rutas_usuario import router as router_usuarios
from app.api.rutas_coordinador import router as router_coordinador
from app.api.rutas_curso import router as router_cursos
from app.api.rutas_primera_clase import router as router_primera_clase
from app.api.rutas_estudiantes import router as router_estudiantes
from app.api.rutas_acudientes import router as router_acudientes
from app.api.rutas_estudxacudiente import router as router_estudxacudiente
from app.api.rutas_motivos import router as router_motivos
from app.api.rutas_asistenciaxestudiante import router as router_asistencia
from app.api.rutas_registronotificaciones import router as router_notificaciones
from app.api.rutas_reportes import router as router_reportes

app = FastAPI(
    title="API de Gestión de llegadas tarde",
    description="Backend modular para el control de llegadas tarde usando FastAPI y PostgreSQL",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_auth)
app.include_router(router_perfiles)
app.include_router(router_modulos)
app.include_router(router_moduloxrol)
app.include_router(router_usuarios)
app.include_router(router_coordinador)
app.include_router(router_cursos)
app.include_router(router_primera_clase)
app.include_router(router_estudiantes)
app.include_router(router_acudientes)
app.include_router(router_estudxacudiente)
app.include_router(router_motivos)
app.include_router(router_asistencia)
app.include_router(router_notificaciones)
app.include_router(router_reportes)

@app.get("/")
def estado_api():
    return {"mensaje": "La API de monitoreo se encuentra en línea y funcional"}

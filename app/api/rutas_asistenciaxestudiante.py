from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from app.core.security import verificar_token
from app.models.asistencia import AsistenciaXEstudiante
from app.repositories.asistencia_repo import AsistenciaXEstudRepository

router = APIRouter(prefix="/api/asistencia", tags=["Gestión de Llegadas Tarde"])
repo = AsistenciaXEstudRepository()

@router.get("/")
def listar(desde: Optional[date] = None, hasta: Optional[date] = None, id_estudiante: Optional[int] = None):
    # Filtros opcionales: /asistencia/?desde=2026-11-01&hasta=2026-11-03
    return repo.obtener_todos(desde, hasta, id_estudiante)

@router.get("/{id_registro}")
def obtener(id_registro: int):
    registro = repo.obtener_por_id(id_registro)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro de llegada tarde no encontrado")
    return registro

@router.post("/")
def crear(registro: AsistenciaXEstudiante, sesion: dict = Depends(verificar_token)):
    # El usuario que registra se toma del token, no del formulario
    registro.id_usuario = int(sesion["sub"])
    nuevo_id, minutos, alerta = repo.crear(registro)
    return {"mensaje": "Llegada tarde registrada", "id": nuevo_id, "minutos_tarde": minutos, "alerta": alerta}

@router.put("/{id_registro}")
def actualizar(id_registro: int, registro: AsistenciaXEstudiante):
    exito = repo.actualizar(id_registro, registro)
    if not exito:
        raise HTTPException(status_code=404, detail="Registro de llegada tarde no encontrado")
    return {"mensaje": "Llegada tarde actualizada"}

@router.delete("/{id_registro}")
def eliminar(id_registro: int):
    exito = repo.eliminar(id_registro)
    if not exito:
        raise HTTPException(status_code=404, detail="Registro de llegada tarde no encontrado")
    return {"mensaje": "Llegada tarde eliminada"}

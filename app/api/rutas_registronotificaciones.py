from fastapi import APIRouter, HTTPException
from app.models.notificacion import RegistroNotificaciones
from app.repositories.notificacion_repo import RegistroNotificacionRepository

router = APIRouter(prefix="/api/notificaciones", tags=["Gestión de Registro de Notificaciones"])
repo = RegistroNotificacionRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/{id_notificacion}")
def obtener_notificacion(id_notificacion: int):
    registro = repo.obtener_por_id(id_notificacion)
    if not registro:
        raise HTTPException(status_code=404, detail="Esa notificación no se encuentra o fue eliminada")
    return registro

@router.post("/")
def crear_notificacion(registro: RegistroNotificaciones):
    nuevo_id = repo.crear(registro)
    return {"mensaje": "Notificación creada", "id": nuevo_id}

@router.put("/{id_notificacion}")
def actualizar(id_notificacion: int, notificacion: RegistroNotificaciones):
    exito = repo.actualizar(id_notificacion, notificacion)
    if not exito:
        raise HTTPException(status_code=404, detail="Registro de notificación no encontrado para actualizar")
    return {"mensaje": "Notificación actualizada"}

@router.delete("/{id_notificacion}")
def eliminar(id_notificacion: int):
    # Borrado lógico: el registro queda con estado = false
    exito = repo.eliminar(id_notificacion)
    if not exito:
        raise HTTPException(status_code=404, detail="No se pudo eliminar, la notificación no existe")
    return {"mensaje": "Notificación inactivada"}

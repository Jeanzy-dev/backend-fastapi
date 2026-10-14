from fastapi import APIRouter, HTTPException
from app.models.registronotificacion import RegistroNotificaciones
from app.repositories.registronotificaciones import RegistroNotificacionRepository

router = APIRouter(prefix="/notificaciones", tags=["Gestión de Registro de Notificaciones"])
repo = RegistroNotificacionRepository()

@router.get("/")
def listar_notificaciones():
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
def actualizar_notificacion(id_notificacion: int, registro: RegistroNotificaciones):
    exito = repo.actualizar(id_notificacion, registro)
    if not exito:
        raise HTTPException(status_code=404, detail="Registro de notificación no encontrado para actualizar")
    return {"mensaje": "Notificación actualizada"}

@router.delete("/{id_notificacion}")
def eliminar_notificacion(id_notificacion: int):
    exito = repo.eliminar(id_notificacion)
    if not exito:
        raise HTTPException(status_code=404, detail="No se pudo eliminar, la notificación no existe")
    return {"mensaje": "Notificación inactivada"}
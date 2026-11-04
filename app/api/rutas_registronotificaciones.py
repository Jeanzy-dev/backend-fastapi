from fastapi import APIRouter, HTTPException
from app.models.notificacion import RegistroNotificaciones
from app.repositories.notificacion_repo import RegistroNotificacionRepository

router = APIRouter(prefix="/api/notificaciones", tags=["Gestión de Registro de Notificaciones"])
repo = RegistroNotificacionRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/{id_notificacion}")
def obtener(id_notificacion: int):
    notificacion = repo.obtener_por_id(id_notificacion)
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return notificacion

@router.post("/")
def crear(notificacion: RegistroNotificaciones):
    nuevo_id = repo.crear(notificacion)
    return {"mensaje": "Notificación registrada exitosamente", "id": nuevo_id}

@router.put("/{id_notificacion}")
def actualizar(id_notificacion: int, notificacion: RegistroNotificaciones):
    exito = repo.actualizar(id_notificacion, notificacion)
    if not exito:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return {"mensaje": "Notificación actualizada correctamente"}

@router.delete("/{id_notificacion}")
def eliminar(id_notificacion: int):
    # Borrado lógico: el registro queda con estado = false
    exito = repo.eliminar(id_notificacion)
    if not exito:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return {"mensaje": "Notificación eliminada correctamente"}

from fastapi import APIRouter, HTTPException
from app.models.acudiente import Acudiente
from app.repositories.acudiente_repo import AcudienteRepository

router = APIRouter(prefix="/acudientes", tags=["Gestión de Acudientes"])
repo = AcudienteRepository()

@router.get("/")
def listar_acudientes():
    return repo.obtener_todos()

@router.get("/{acudiente_id}")
def obtener_acudiente(acudiente_id: int):
    acudiente = repo.obtener_por_id(acudiente_id)
    if not acudiente:
        raise HTTPException(status_code=404, detail="Acudiente no encontrado")
    return acudiente

@router.post("/")
def crear_acudiente(acudiente: Acudiente):
    nuevo_id = repo.crear(acudiente)
    return {"mensaje": "Acudiente registrado exitosamente", "id": nuevo_id}

@router.delete("/{acudiente_id}")
def eliminar_acudiente(acudiente_id: int):
    exito = repo.eliminar(acudiente_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Acudiente no encontrado")
    return {"mensaje": "Acudiente eliminado correctamente"}

@router.put("/{acudiente_id}")
def actualizar_acudiente(acudiente_id: int, acudiente: Acudiente):
    exito = repo.actualizar(acudiente_id, acudiente)
    if not exito:
        raise HTTPException(status_code=404, detail="Acudiente no encontrado")
    return {"mensaje": "Acudiente actualizado correctamente"}
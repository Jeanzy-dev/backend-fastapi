from fastapi import APIRouter, HTTPException
from app.models.acudiente import Acudiente
from app.repositories.acudiente_repo import AcudienteRepository

router = APIRouter(prefix="/api/acudientes", tags=["Gestión de Acudientes"])
repo = AcudienteRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/{acudiente_id}")
def obtener(acudiente_id: int):
    acudiente = repo.obtener_por_id(acudiente_id)
    if not acudiente:
        raise HTTPException(status_code=404, detail="Acudiente no encontrado")
    return acudiente

@router.post("/")
def crear(acudiente: Acudiente):
    nuevo_id = repo.crear(acudiente)
    return {"mensaje": "Acudiente registrado exitosamente", "id": nuevo_id}

@router.put("/{acudiente_id}")
def actualizar(acudiente_id: int, acudiente: Acudiente):
    exito = repo.actualizar(acudiente_id, acudiente)
    if not exito:
        raise HTTPException(status_code=404, detail="Acudiente no encontrado")
    return {"mensaje": "Acudiente actualizado correctamente"}

@router.delete("/{acudiente_id}")
def eliminar(acudiente_id: int):
    # Borrado lógico: el registro queda con estado = false
    exito = repo.eliminar(acudiente_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Acudiente no encontrado")
    return {"mensaje": "Acudiente eliminado correctamente"}

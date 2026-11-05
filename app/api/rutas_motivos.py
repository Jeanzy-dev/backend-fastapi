from fastapi import APIRouter, HTTPException
from app.models.motivo import MotivoTardanza
from app.repositories.motivo_repo import MotivoRepository

router = APIRouter(prefix="/api/motivos", tags=["Gestión de Motivos"])
repo = MotivoRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/{motivo_id}")
def obtener(motivo_id: int):
    motivo = repo.obtener_por_id(motivo_id)
    if not motivo:
        raise HTTPException(status_code=404, detail="Motivo no encontrado")
    return motivo

@router.post("/")
def crear(motivo: MotivoTardanza):
    nuevo_id = repo.crear(motivo)
    return {"mensaje": "Motivo registrado exitosamente", "id": nuevo_id}

@router.put("/{motivo_id}")
def actualizar(motivo_id: int, motivo: MotivoTardanza):
    exito = repo.actualizar(motivo_id, motivo)
    if not exito:
        raise HTTPException(status_code=404, detail="Motivo no encontrado")
    return {"mensaje": "Motivo actualizado correctamente"}

@router.delete("/{motivo_id}")
def eliminar(motivo_id: int):
    # Borrado lógico: el registro queda con estado = false
    exito = repo.eliminar(motivo_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Motivo no encontrado")
    return {"mensaje": "Motivo eliminado correctamente"}

from fastapi import APIRouter, HTTPException
from app.models.motivo import MotivoTardanza
from app.repositories.motivo_repo import MotivoRepository

router = APIRouter(prefix="/motivos", tags=["Gestión de Motivos"])
repo = MotivoRepository()

@router.get("/")
def listar_motivos():
    return repo.obtener_todos()

@router.get("/{motivo_id}")
def obtener_motivo(motivo_id: int):
    motivo = repo.obtener_por_id(motivo_id)
    if not motivo:
        raise HTTPException(status_code=404, detail="Motivo no encontrado")
    return motivo

@router.post("/")
def crear_motivo(motivo: MotivoTardanza):
    nuevo_id = repo.crear(motivo)
    return {"mensaje": "Motivo registrado exitosamente", "id": nuevo_id}

@router.delete("/{motivo_id}")
def eliminar_motivo(motivo_id: int):
    exito = repo.eliminar(motivo_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Motivo no encontrado")
    return {"mensaje": "Motivo eliminado correctamente"}

@router.put("/{motivo_id}")
def actualizar_motivo(motivo_id: int, motivo: MotivoTardanza):
    exito = repo.actualizar(motivo_id, motivo)
    if not exito:
        raise HTTPException(status_code=404, detail="Motivo no encontrado")
    return {"mensaje": "Motivo actualizado correctamente"}
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.motivo import MotivoCrear, MotivoRespuesta
from app.repositories.motivo_repo import MotivoRepository

router = APIRouter(prefix="/motivos", tags=["Gestión de Motivos de Tardanza"])
repo = MotivoRepository()

@router.get("/", response_model=List[MotivoRespuesta], summary="Listar motivos activos")
def listar_motivos():
    return repo.obtener_todos()

@router.get("/{id_motivo}", response_model=MotivoRespuesta, summary="Obtener motivo por ID")
def obtener_motivo(id_motivo: int):
    motivo = repo.obtener_por_id(id_motivo)
    if not motivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motivo no encontrado o inactivo")
    return motivo

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Crear motivo")
def crear_motivo(motivo: MotivoCrear):
    nuevo_id = repo.crear(motivo)
    return {"mensaje": "Motivo creado exitosamente", "id_motivo": nuevo_id}

@router.put("/{id_motivo}", summary="Actualizar motivo")
def actualizar_motivo(id_motivo: int, motivo: MotivoCrear):
    exito = repo.actualizar(id_motivo, motivo)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motivo no encontrado o inactivo")
    return {"mensaje": "Motivo actualizado exitosamente"}

@router.delete("/{id_motivo}", summary="Eliminar motivo (Lógico)")
def eliminar_motivo(id_motivo: int):
    exito = repo.eliminar_logico(id_motivo)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motivo no encontrado o ya inactivo")
    return {"mensaje": f"Motivo con id {id_motivo} desactivado exitosamente (Soft Delete)"}
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.acudiente import AcudienteCrear, AcudienteRespuesta
from app.repositories.acudiente_repo import AcudienteRepository

router = APIRouter(prefix="/acudientes", tags=["Gestión de Acudientes"])
repo = AcudienteRepository()

@router.get("/", response_model=List[AcudienteRespuesta], summary="Listar acudientes activos")
def listar_acudientes():
    return repo.obtener_todos()

@router.get("/{id_acudiente}", response_model=AcudienteRespuesta, summary="Obtener acudiente por ID")
def obtener_acudiente(id_acudiente: int):
    acudiente = repo.obtener_por_id(id_acudiente)
    if not acudiente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Acudiente no encontrado o inactivo")
    return acudiente

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Crear acudiente")
def crear_acudiente(acudiente: AcudienteCrear):
    nuevo_id = repo.crear(acudiente)
    return {"mensaje": "Acudiente registrado exitosamente", "id_acudiente": nuevo_id}

@router.put("/{id_acudiente}", summary="Actualizar acudiente")
def actualizar_acudiente(id_acudiente: int, acudiente: AcudienteCrear):
    exito = repo.actualizar(id_acudiente, acudiente)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Acudiente no encontrado o inactivo")
    return {"mensaje": "Acudiente actualizado exitosamente"}

@router.delete("/{id_acudiente}", summary="Eliminar acudiente (Lógico)")
def eliminar_acudiente(id_acudiente: int):
    exito = repo.eliminar_logico(id_acudiente)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Acudiente no encontrado o ya inactivo")
    return {"mensaje": f"Acudiente con id {id_acudiente} desactivado exitosamente (Soft Delete)"}
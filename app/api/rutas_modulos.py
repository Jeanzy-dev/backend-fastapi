from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.modulo import ModuloCrear, ModuloRespuesta
from app.repositories.modulo_repo import ModuloRepository

router = APIRouter(prefix="/modulos", tags=["Gestión de Módulos"])
repo = ModuloRepository()

@router.get("/", response_model=List[ModuloRespuesta], summary="Listar módulos activos")
def listar_modulos():
    return repo.obtener_todos()

@router.get("/{id_modulo}", response_model=ModuloRespuesta, summary="Obtener módulo por ID")
def obtener_modulo(id_modulo: int):
    modulo = repo.obtener_por_id(id_modulo)
    if not modulo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Módulo no encontrado o inactivo")
    return modulo

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Crear nuevo módulo")
def crear_modulo(modulo: ModuloCrear):
    nuevo_id = repo.crear(modulo)
    return {"mensaje": "Módulo creado exitosamente", "id_modulo": nuevo_id}

@router.put("/{id_modulo}", summary="Actualizar módulo")
def actualizar_modulo(id_modulo: int, modulo: ModuloCrear):
    exito = repo.actualizar(id_modulo, modulo)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Módulo no encontrado o inactivo")
    return {"mensaje": "Módulo actualizado exitosamente"}

@router.delete("/{id_modulo}", summary="Eliminar módulo (Lógico)")
def eliminar_modulo(id_modulo: int):
    exito = repo.eliminar_logico(id_modulo)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Módulo no encontrado o ya inactivo")
    return {"mensaje": f"Módulo con id {id_modulo} desactivado exitosamente (Soft Delete)"}
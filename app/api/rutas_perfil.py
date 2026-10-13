from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.perfil import PerfilCrear, PerfilRespuesta
from app.repositories.perfil_repo import PerfilRepository

router = APIRouter(prefix="/perfiles", tags=["Gestión de Perfiles"])
repo = PerfilRepository()

@router.get("/", response_model=List[PerfilRespuesta], summary="Listar perfiles activos")
def listar_perfiles():
    return repo.obtener_todos()

@router.get("/{id_perfil}", response_model=PerfilRespuesta, summary="Obtener perfil por ID")
def obtener_perfil(id_perfil: int):
    perfil = repo.obtener_por_id(id_perfil)
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")
    return perfil

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Crear nuevo perfil")
def crear_perfil(perfil: PerfilCrear):
    nuevo_id = repo.crear(perfil)
    return {"mensaje": "Perfil creado con éxito", "id_perfil": nuevo_id}

@router.put("/{id_perfil}", summary="Actualizar perfil")
def actualizar_perfil(id_perfil: int, perfil: PerfilCrear):
    exito = repo.actualizar(id_perfil, perfil)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado o inactivo")
    return {"mensaje": "Perfil actualizado con éxito"}

@router.delete("/{id_perfil}", summary="Eliminar perfil (Lógico)")
def eliminar_perfil(id_perfil: int):
    exito = repo.eliminar_logico(id_perfil)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado o ya inactivo")
    return {"mensaje": f"Perfil con id {id_perfil} desactivado exitosamente (Soft Delete)"}
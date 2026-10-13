from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.primera_clase import PrimeraClaseCrear, PrimeraClaseRespuesta
from app.repositories.primera_clase_repo import PrimeraClaseRepository

router = APIRouter(prefix="/horarios-grupos", tags=["Gestión de Horarios por Grupo (Primera Clase)"])
repo = PrimeraClaseRepository()

@router.get("/", response_model=List[PrimeraClaseRespuesta], summary="Listar horarios activos")
def listar_horarios():
    return repo.obtener_todos()

@router.get("/{id_clase_grupo}", response_model=PrimeraClaseRespuesta, summary="Obtener horario por ID")
def obtener_horario(id_clase_grupo: int):
    horario = repo.obtener_por_id(id_clase_grupo)
    if not horario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario no encontrado o inactivo")
    return horario

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Crear horario para grupo")
def crear_horario(horario: PrimeraClaseCrear):
    nuevo_id = repo.crear(horario)
    return {"mensaje": "Horario registrado exitosamente", "id_clase_grupo": nuevo_id}

@router.put("/{id_clase_grupo}", summary="Actualizar horario")
def actualizar_horario(id_clase_grupo: int, horario: PrimeraClaseCrear):
    exito = repo.actualizar(id_clase_grupo, horario)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario no encontrado o inactivo")
    return {"mensaje": "Horario actualizado exitosamente"}

@router.delete("/{id_clase_grupo}", summary="Eliminar horario (Lógico)")
def eliminar_horario(id_clase_grupo: int):
    exito = repo.eliminar_logico(id_clase_grupo)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario no encontrado o ya inactivo")
    return {"mensaje": f"Horario con id {id_clase_grupo} desactivado exitosamente (Soft Delete)"}
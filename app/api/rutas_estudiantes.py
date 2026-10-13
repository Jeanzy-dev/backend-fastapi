from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.estudiante import EstudianteCrear, EstudianteRespuesta
from app.repositories.estudiante_repo import EstudianteRepository

router = APIRouter(prefix="/estudiantes", tags=["Gestión de Estudiantes"])
repo = EstudianteRepository()

@router.get("/", response_model=List[EstudianteRespuesta], summary="Listar estudiantes activos")
def listar_estudiantes():
    return repo.obtener_todos()

@router.get("/{id_estudiante}", response_model=EstudianteRespuesta, summary="Obtener estudiante por ID")
def obtener_estudiante(id_estudiante: int):
    estudiante = repo.obtener_por_id(id_estudiante)
    if not estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado o inactivo")
    return estudiante

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Crear estudiante")
def crear_estudiante(estudiante: EstudianteCrear):
    nuevo_id = repo.crear(estudiante)
    return {"mensaje": "Estudiante registrado exitosamente", "id_estudiante": nuevo_id}

@router.put("/{id_estudiante}", summary="Actualizar estudiante")
def actualizar_estudiante(id_estudiante: int, estudiante: EstudianteCrear):
    exito = repo.actualizar(id_estudiante, estudiante)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado o inactivo")
    return {"mensaje": "Estudiante actualizado exitosamente"}

@router.delete("/{id_estudiante}", summary="Eliminar estudiante (Lógico)")
def eliminar_estudiante(id_estudiante: int):
    exito = repo.eliminar_logico(id_estudiante)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado o ya inactivo")
    return {"mensaje": f"Estudiante con id {id_estudiante} desactivado exitosamente (Soft Delete)"}
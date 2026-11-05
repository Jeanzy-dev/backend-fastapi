from fastapi import APIRouter, HTTPException
from app.models.estudiante import Estudiante
from app.repositories.estudiante_repo import EstudianteRepository

router = APIRouter(prefix="/api/estudiantes", tags=["Gestión de Estudiantes"])
repo = EstudianteRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/{estudiante_id}")
def obtener(estudiante_id: int):
    estudiante = repo.obtener_por_id(estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante

@router.post("/")
def crear(estudiante: Estudiante):
    nuevo_id = repo.crear(estudiante)
    return {"mensaje": "Estudiante registrado exitosamente", "id": nuevo_id}

@router.put("/{estudiante_id}")
def actualizar(estudiante_id: int, estudiante: Estudiante):
    exito = repo.actualizar(estudiante_id, estudiante)
    if not exito:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"mensaje": "Estudiante actualizado correctamente"}

@router.delete("/{estudiante_id}")
def eliminar(estudiante_id: int):
    # Borrado lógico: el registro queda con estado = false
    exito = repo.eliminar(estudiante_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"mensaje": "Estudiante eliminado correctamente"}

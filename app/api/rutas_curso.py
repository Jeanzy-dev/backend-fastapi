from fastapi import APIRouter, HTTPException
from app.models.curso import Curso
from app.repositories.curso_repo import CursoRepository

router = APIRouter(prefix="/api/cursos", tags=["Gestión de Cursos"])
repo = CursoRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/{curso_id}")
def obtener(curso_id: int):
    curso = repo.obtener_por_id(curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.post("/")
def crear(curso: Curso):
    nuevo_id = repo.crear(curso)
    return {"mensaje": "Curso registrado exitosamente", "id": nuevo_id}

@router.put("/{curso_id}")
def actualizar(curso_id: int, curso: Curso):
    exito = repo.actualizar(curso_id, curso)
    if not exito:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"mensaje": "Curso actualizado correctamente"}

@router.delete("/{curso_id}")
def eliminar(curso_id: int):
    # Borrado lógico: el registro queda con estado = false
    exito = repo.eliminar(curso_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"mensaje": "Curso eliminado correctamente"}

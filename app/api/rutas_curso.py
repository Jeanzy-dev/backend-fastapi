from fastapi import APIRouter, HTTPException
from app.models.curso import Curso
from app.repositories.curso_repo import CursoRepository

router = APIRouter(prefix="/cursos", tags=["Gestión de Cursos"])
repo = CursoRepository()

@router.get("/")
def listar_cursos():
    return repo.obtener_todos()

@router.get("/{curso_id}")
def obtener_curso(curso_id: int):
    curso = repo.obtener_por_id(curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.post("/")
def crear_curso(curso: Curso):
    nuevo_id = repo.crear(curso)
    return {"mensaje": "Curso registrado exitosamente", "id": nuevo_id}

@router.delete("/{curso_id}")
def eliminar_curso(curso_id: int):
    exito = repo.eliminar(curso_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"mensaje": "Curso eliminado correctamente"}

@router.put("/{curso_id}")
def actualizar_curso(curso_id: int, curso: Curso):
    exito = repo.actualizar(curso_id, curso)
    if not exito:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"mensaje": "Curso actualizado correctamente"}
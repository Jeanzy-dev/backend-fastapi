from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.curso import CursoCrear, CursoRespuesta
from app.repositories.curso_repo import CursoRepository

router = APIRouter(prefix="/cursos", tags=["Gestión de Cursos"])
repo = CursoRepository()

@router.get("/", response_model=List[CursoRespuesta], summary="Listar cursos activos")
def listar_cursos():
    return repo.obtener_todos()

@router.get("/{id_curso}", response_model=CursoRespuesta, summary="Obtener curso por ID")
def obtener_curso(id_curso: int):
    curso = repo.obtener_por_id(id_curso)
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado o inactivo")
    return curso

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Crear nuevo curso")
def crear_curso(curso: CursoCrear):
    nuevo_id = repo.crear(curso)
    return {"mensaje": "Curso creado exitosamente", "id_curso": nuevo_id}

@router.put("/{id_curso}", summary="Actualizar curso")
def actualizar_curso(id_curso: int, curso: CursoCrear):
    exito = repo.actualizar(id_curso, curso)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado o inactivo")
    return {"mensaje": "Curso actualizado exitosamente"}

@router.delete("/{id_curso}", summary="Eliminar curso (Lógico)")
def eliminar_curso(id_curso: int):
    exito = repo.eliminar_logico(id_curso)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado o ya inactivo")
    return {"mensaje": f"Curso con id {id_curso} desactivado exitosamente (Soft Delete)"}
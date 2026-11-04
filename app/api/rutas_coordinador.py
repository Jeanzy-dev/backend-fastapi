from fastapi import APIRouter, HTTPException
from app.models.coordinador import Coordinador
from app.repositories.coordinador_repo import CoordinadorRepository

router = APIRouter(prefix="/api/coordinador", tags=["Gestión de Coordinadores"])
repo = CoordinadorRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/{id_coordinador}")
def obtener(id_coordinador: int):
    coordinador = repo.obtener_por_id(id_coordinador)
    if not coordinador:
        raise HTTPException(status_code=404, detail="Coordinador no encontrado")
    return coordinador

@router.post("/")
def crear(coordinador: Coordinador):
    nuevo_id = repo.crear(coordinador)
    return {"mensaje": "Coordinador registrado exitosamente", "id": nuevo_id}

@router.put("/{id_coordinador}")
def actualizar(id_coordinador: int, coordinador: Coordinador):
    exito = repo.actualizar(id_coordinador, coordinador)
    if not exito:
        raise HTTPException(status_code=404, detail="Coordinador no encontrado")
    return {"mensaje": "Coordinador actualizado correctamente"}

@router.delete("/{id_coordinador}")
def eliminar(id_coordinador: int):
    # Borrado lógico: el registro queda con estado = false
    exito = repo.eliminar(id_coordinador)
    if not exito:
        raise HTTPException(status_code=404, detail="Coordinador no encontrado")
    return {"mensaje": "Coordinador eliminado correctamente"}

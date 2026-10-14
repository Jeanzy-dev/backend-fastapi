from fastapi import APIRouter, HTTPException
from app.models.coordinador import Coordinador
from app.repositories.coordinador import CoordinadorRepository

router = APIRouter(prefix="/coordinador", tags=["Gestión de Coordinadores"])
repo = CoordinadorRepository()

@router.get("/")
def listar_coordinadores():
    return repo.obtener_todos()

@router.get("/{id_coordinador}")
def obtener_coordinador(id_coordinador: int):
    registro = repo.obtener_por_id(id_coordinador)
    if not registro:
        raise HTTPException(status_code=404, detail="El coordinador no se encuentra o ha sido eliminado")
    return registro

@router.post("/")
def crear_coordinador(registro: Coordinador):
    nuevo_id = repo.crear(registro)
    return {"mensaje": "Coordinador creado correctamente", "id": nuevo_id}

@router.put("/{id_coordinador}")
def actualizar_coordinador(id_coordinador: int, registro: Coordinador):
    exito = repo.actualizar(id_coordinador, registro)
    if not exito:
        raise HTTPException(status_code=404, detail="Coordinador no encontrado para actualizar")
    return {"mensaje": "Coordinador actualizado correctamente"}

@router.delete("/{id_coordinador}")
def eliminar_coordinador(id_coordinador: int):
    exito = repo.eliminar(id_coordinador)
    if not exito:
        raise HTTPException(status_code=404, detail="No se pudo eliminar, el coordinador no existe")
    return {"mensaje": "Coordinador inactivado correctamente"}
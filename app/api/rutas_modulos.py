from fastapi import APIRouter, HTTPException
from app.models.modulo import Modulo
from app.repositories.modulo_repo import ModuloRepository

router = APIRouter(prefix="/api/modulos", tags=["Gestión de Módulos"])
repo = ModuloRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/{modulo_id}")
def obtener(modulo_id: int):
    modulo = repo.obtener_por_id(modulo_id)
    if not modulo:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    return modulo

@router.post("/")
def crear(modulo: Modulo):
    nuevo_id = repo.crear(modulo)
    return {"mensaje": "Módulo registrado exitosamente", "id": nuevo_id}

@router.put("/{modulo_id}")
def actualizar(modulo_id: int, modulo: Modulo):
    exito = repo.actualizar(modulo_id, modulo)
    if not exito:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    return {"mensaje": "Módulo actualizado correctamente"}

@router.delete("/{modulo_id}")
def eliminar(modulo_id: int):
    # Borrado lógico: el registro queda con estado = false
    exito = repo.eliminar(modulo_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    return {"mensaje": "Módulo eliminado correctamente"}

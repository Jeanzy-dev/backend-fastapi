from fastapi import APIRouter, HTTPException
from app.models.perfil import Perfil
from app.repositories.perfil_repo import PerfilRepository

router = APIRouter(prefix="/api/perfiles", tags=["Gestión de Perfiles"])
repo = PerfilRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/{perfil_id}")
def obtener(perfil_id: int):
    perfil = repo.obtener_por_id(perfil_id)
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return perfil

@router.post("/")
def crear(perfil: Perfil):
    nuevo_id = repo.crear(perfil)
    return {"mensaje": "Perfil registrado exitosamente", "id": nuevo_id}

@router.put("/{perfil_id}")
def actualizar(perfil_id: int, perfil: Perfil):
    exito = repo.actualizar(perfil_id, perfil)
    if not exito:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return {"mensaje": "Perfil actualizado correctamente"}

@router.delete("/{perfil_id}")
def eliminar(perfil_id: int):
    # Borrado lógico: el registro queda con estado = false
    exito = repo.eliminar(perfil_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return {"mensaje": "Perfil eliminado correctamente"}

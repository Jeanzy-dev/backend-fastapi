from fastapi import APIRouter, HTTPException
from app.models.perfil import Perfil
from app.repositories.perfil_repo import PerfilRepository

router = APIRouter(prefix="/perfiles", tags=["Gestión de Perfiles"])
repo = PerfilRepository()

@router.get("/")
def listar_perfiles():
    return repo.obtener_todos()

@router.get("/{perfil_id}")
def obtener_perfil(perfil_id: int):
    perfil = repo.obtener_por_id(perfil_id)
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return perfil

@router.post("/")
def crear_perfil(perfil: Perfil):
    nuevo_id = repo.crear(perfil)
    return {"mensaje": "Perfil registrado exitosamente", "id": nuevo_id}

@router.delete("/{perfil_id}")
def eliminar_perfil(perfil_id: int):
    exito = repo.eliminar(perfil_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return {"mensaje": "Perfil eliminado correctamente"}

@router.put("/{perfil_id}")
def actualizar_perfil(perfil_id: int, perfil: Perfil):
    exito = repo.actualizar(perfil_id, perfil)
    if not exito:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return {"mensaje": "Perfil actualizado correctamente"}
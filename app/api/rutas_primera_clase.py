from fastapi import APIRouter, HTTPException
from app.models.primera_clase import PrimeraClase
from app.repositories.primera_clase_repo import PrimeraClaseRepository

router = APIRouter(prefix="/primera-clase", tags=["Gestión de Primera Clase"])
repo = PrimeraClaseRepository()

@router.get("/")
def listar_clases():
    return repo.obtener_todos()

@router.get("/{clase_id}")
def obtener_clase(clase_id: int):
    clase = repo.obtener_por_id(clase_id)
    if not clase:
        raise HTTPException(status_code=404, detail="Primera clase no encontrada")
    return clase

@router.post("/")
def crear_clase(clase: PrimeraClase):
    nuevo_id = repo.crear(clase)
    return {"mensaje": "Primera clase registrada exitosamente", "id": nuevo_id}

@router.delete("/{clase_id}")
def eliminar_clase(clase_id: int):
    exito = repo.eliminar(clase_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Primera clase no encontrada")
    return {"mensaje": "Primera clase eliminada correctamente"}

@router.put("/{clase_id}")
def actualizar_clase(clase_id: int, clase: PrimeraClase):
    exito = repo.actualizar(clase_id, clase)
    if not exito:
        raise HTTPException(status_code=404, detail="Primera clase no encontrada")
    return {"mensaje": "Primera clase actualizada correctamente"}
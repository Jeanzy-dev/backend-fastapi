from fastapi import APIRouter, HTTPException
from app.models.primera_clase import PrimeraClase
from app.repositories.primera_clase_repo import PrimeraClaseRepository

router = APIRouter(prefix="/api/primera-clase", tags=["Gestión de Primera Clase"])
repo = PrimeraClaseRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/{clase_id}")
def obtener(clase_id: int):
    clase = repo.obtener_por_id(clase_id)
    if not clase:
        raise HTTPException(status_code=404, detail="Horario de primera clase no encontrado")
    return clase

@router.post("/")
def crear(clase: PrimeraClase):
    nuevo_id = repo.crear(clase)
    return {"mensaje": "Horario de primera clase registrado exitosamente", "id": nuevo_id}

@router.put("/{clase_id}")
def actualizar(clase_id: int, clase: PrimeraClase):
    exito = repo.actualizar(clase_id, clase)
    if not exito:
        raise HTTPException(status_code=404, detail="Horario de primera clase no encontrado")
    return {"mensaje": "Horario de primera clase actualizado correctamente"}

@router.delete("/{clase_id}")
def eliminar(clase_id: int):
    # Borrado lógico: el registro queda con estado = false
    exito = repo.eliminar(clase_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Horario de primera clase no encontrado")
    return {"mensaje": "Horario de primera clase eliminado correctamente"}

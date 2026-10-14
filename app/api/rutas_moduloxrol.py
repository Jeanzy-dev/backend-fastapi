from fastapi import APIRouter, HTTPException
from app.models.moduloxrol import ModuloxRol
from app.repositories.moduloxrol import ModuloxRolRepository

router = APIRouter(prefix="/moduloxrol", tags=["Gestión de Módulo x Rol"])
repo = ModuloxRolRepository()

@router.get("/")
def listar_modulos_rol():
    return repo.obtener_todos()

@router.get("/{id_registro}")
def obtener_modulo_rol(id_registro: int):
    registro = repo.obtener_por_id(id_registro)
    if not registro:
        raise HTTPException(status_code=404, detail="Ese registro no existe o fue eliminado")
    return registro

@router.post("/")
def crear_modulo_rol(registro: ModuloxRol):
    nuevo_id = repo.crear(registro)
    return {"mensaje": "Módulo por rol creado", "id": nuevo_id}

@router.put("/{id_registro}")
def actualizar_modulo_rol(id_registro: int, registro: ModuloxRol):
    exito = repo.actualizar(id_registro, registro)
    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado para actualizar")
    return {"mensaje": "Módulo por rol actualizado"}

@router.delete("/{id_registro}")
def eliminar_modulo_rol(id_registro: int):
    exito = repo.eliminar(id_registro)
    if not exito:
        raise HTTPException(status_code=404, detail="No se pudo eliminar, el modulo no existe")
    return {"mensaje": "Registro inactivado"}
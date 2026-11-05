from fastapi import APIRouter, HTTPException
from app.models.moduloxrol import ModuloxRol
from app.repositories.moduloxrol_repo import ModuloxRolRepository

router = APIRouter(prefix="/api/moduloxrol", tags=["Gestión de Módulo x Rol"])
repo = ModuloxRolRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/perfil/{id_perfil}")
def modulos_del_perfil(id_perfil: int):
    # El frontend arma el menú con esta respuesta (tabla moduloxrol)
    return repo.obtener_por_perfil(id_perfil)

@router.get("/{id_registro}")
def obtener(id_registro: int):
    registro = repo.obtener_por_id(id_registro)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

@router.post("/")
def crear(registro: ModuloxRol):
    nuevo_id = repo.crear(registro)
    return {"mensaje": "Módulo asignado al perfil", "id": nuevo_id}

@router.put("/{id_registro}")
def actualizar(id_registro: int, registro: ModuloxRol):
    exito = repo.actualizar(id_registro, registro)
    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"mensaje": "Asignación actualizada"}

@router.delete("/{id_registro}")
def eliminar(id_registro: int):
    exito = repo.eliminar(id_registro)
    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"mensaje": "Asignación eliminada"}

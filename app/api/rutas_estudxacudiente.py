from fastapi import APIRouter, HTTPException
from app.models.estudxacudiente import EstudXAcudiente
from app.repositories.estudxacudiente_repo import EstudXAcudienteRepository

router = APIRouter(prefix="/api/estudxacudiente", tags=["Gestión de Estudiante x Acudiente"])
repo = EstudXAcudienteRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/{id_registro}")
def obtener(id_registro: int):
    registro = repo.obtener_por_id(id_registro)
    if not registro:
        raise HTTPException(status_code=404, detail="Ese registro no se encuentra o lo borraron")
    return registro

@router.post("/")
def crear(registro: EstudXAcudiente):
    nuevo_id = repo.crear(registro)
    return {"mensaje": "Relación estudiante-acudiente creada", "id": nuevo_id}

@router.put("/{id_registro}")
def actualizar(id_registro: int, registro: EstudXAcudiente):
    exito = repo.actualizar(id_registro, registro)
    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado para actualizar")
    return {"mensaje": "Registro actualizado"}

@router.delete("/{id_registro}")
def eliminar(id_registro: int):
    # Borrado lógico: el registro queda con estado = false
    exito = repo.eliminar(id_registro)
    if not exito:
        raise HTTPException(status_code=404, detail="No se pudo eliminar, el estudiante no existe")
    return {"mensaje": "Registro inactivado"}

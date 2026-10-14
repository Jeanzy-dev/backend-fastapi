from fastapi import APIRouter, HTTPException
from app.models.estudxacudiente import EstudXAcudiente
from app.repositories.estudxacudiente import EstudXAcudienteRepository

router = APIRouter(prefix="/estudxacudiente", tags=["Gestión de Estudiante x Acudiente"])
repo = EstudXAcudienteRepository()

@router.get("/")
def listar_estudiantes_acudientes():
    return repo.obtener_todos()

@router.get("/{id_registro}")
def obtener_estudiante_acudiente(id_registro: int):
    registro = repo.obtener_por_id(id_registro)
    if not registro:
        raise HTTPException(status_code=404, detail="Ese registro no se encuentra o lo borraron")
    return registro

@router.post("/")
def crear_estudiante_acudiente(registro: EstudXAcudiente):
    nuevo_id = repo.crear(registro)
    return {"mensaje": "Relación estudiante-acudiente creada", "id": nuevo_id}

@router.put("/{id_registro}")
def actualizar_estudiante_acudiente(id_registro: int, registro: EstudXAcudiente):
    exito = repo.actualizar(id_registro, registro)
    if not exito:
        raise HTTPException(status_code=404, detail="Registro no encontrado para actualizar")
    return {"mensaje": "Registro actualizado"}

@router.delete("/{id_registro}")
def eliminar_estudiante_acudiente(id_registro: int):
    exito = repo.eliminar(id_registro)
    if not exito:
        raise HTTPException(status_code=404, detail="No se pudo eliminar, el estudiante no existe")
    return {"mensaje": "Registro inactivado"}
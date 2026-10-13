from fastapi import APIRouter, HTTPException
from app.models.asistenciaxestud import AsistenciaXEstudiante
from app.repositories.asistenciaxestudiante import AsistenciaXEstudRepository

router = APIRouter(prefix="/asistencia", tags=["Gestión de Asistencia por Estudiante"])
repo = AsistenciaXEstudRepository()

@router.get("/")
def listar_asistencias():
    return repo.obtener_todos()

@router.get("/{id_registro}")
def obtener_asistencia(id_registro: int):
    registro = repo.obtener_por_id(id_registro)
    if not registro:
        raise HTTPException(status_code=404, detail="Eche, esa asistencia no se encuentra o la borraron")
    return registro

@router.post("/")
def crear_asistencia(registro: AsistenciaXEstudiante):
    nuevo_id = repo.crear(registro)
    return {"mensaje": "Asistencia registrada del putas", "id": nuevo_id}

@router.put("/{id_registro}")
def actualizar_asistencia(id_registro: int, registro: AsistenciaXEstudiante):
    exito = repo.actualizar(id_registro, registro)
    if not exito:
        raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado pa' actualizar")
    return {"mensaje": "Asistencia actualizada bacano"}

@router.delete("/{id_registro}")
def eliminar_asistencia(id_registro: int):
    exito = repo.eliminar(id_registro)
    if not exito:
        raise HTTPException(status_code=404, detail="No se pudo eliminar, el man no existe")
    return {"mensaje": "Asistencia inactivada melo (borrado lógico aplicado)"}
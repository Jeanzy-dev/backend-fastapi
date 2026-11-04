from fastapi import APIRouter, HTTPException
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository

router = APIRouter(prefix="/api/usuarios", tags=["Gestión de Usuarios"])
repo = UsuarioRepository()

@router.get("/")
def listar():
    return repo.obtener_todos()

@router.get("/{id_usuario}")
def obtener(id_usuario: int):
    usuario = repo.obtener_por_id(id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/")
def crear(usuario: Usuario):
    if not usuario.password:
        raise HTTPException(status_code=422, detail="La contraseña es obligatoria")
    nuevo_id = repo.crear(usuario)
    return {"mensaje": "Usuario registrado exitosamente", "id": nuevo_id}

@router.put("/{id_usuario}")
def actualizar(id_usuario: int, usuario: Usuario):
    exito = repo.actualizar(id_usuario, usuario)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado para actualizar")
    return {"mensaje": "Usuario actualizado"}

@router.delete("/{id_usuario}")
def eliminar(id_usuario: int):
    # Borrado lógico: el registro queda con estado = false
    exito = repo.eliminar(id_usuario)
    if not exito:
        raise HTTPException(status_code=404, detail="No se pudo eliminar, el usuario no existe")
    return {"mensaje": "Usuario inactivado"}

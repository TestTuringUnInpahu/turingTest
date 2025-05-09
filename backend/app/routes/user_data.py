from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()

user_sessions = {}

class DatosPersonales(BaseModel):
    nombre: str
    edad: int
    nacionalidad: str
    idioma: str

@router.post("/datos_personales")
async def guardar_datos_personales(data: DatosPersonales, request: Request):
    ip = request.client.host
    user_sessions[ip] = {
    "nombre": data.nombre,
    "edad": data.edad,
    "nacionalidad": data.nacionalidad,
    "idioma": data.idioma,
    "autorizado": True
    }
    return {"mensaje": "Datos personales guardados correctamente"}

@router.get("/verificar_datos")
async def verificar_datos(request: Request):
    ip = request.client.host
    
    # Verificamos si los datos del usuario están en la sesión
    if ip not in user_sessions or not user_sessions[ip]["autorizado"]:
        raise HTTPException(status_code=400, detail="Debe completar los datos personales antes de usar el chat")
    
    return {"mensaje": "Datos personales completos y autorización para el chat concedida"}
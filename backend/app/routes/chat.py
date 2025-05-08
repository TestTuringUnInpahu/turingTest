import asyncio
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini_service import generar_respuesta
from app.utils.logger import guardar_en_txt

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str
    
    
def estimar_tiempo_respuesta(texto: str, palabras_por_segundo: float = 1.5) -> float:
    palabras = len(texto.split())
    tiempo_estimado = palabras / palabras_por_segundo
    return round(tiempo_estimado, 2)

@router.post("/chat")
async def chat_with_gemini(request: PromptRequest):
    try:
        respuesta = generar_respuesta(request.prompt)
        guardar_en_txt(request.prompt, respuesta)
        
        num_palabras = len(respuesta.split())
        palabras_por_segundo = 2
        tiempo_estimado = round(num_palabras / palabras_por_segundo, 1)
        
        await asyncio.sleep(tiempo_estimado)
        
        return {
            "response": respuesta,
            "tiempo_estimado_respuesta": tiempo_estimado
            }
    except Exception as e:
        return {"error": str(e)}
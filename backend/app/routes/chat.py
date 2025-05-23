import asyncio
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.services.gemini_service import generar_respuesta
from app.utils.logger import guardar_en_txt
from app.routes.user_data import user_sessions

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str
    
def estimar_tiempo_respuesta(texto: str, palabras_por_segundo: float = 1.5) -> float:
    palabras = len(texto.split())
    tiempo_estimado = palabras / palabras_por_segundo
    return round(tiempo_estimado, 2)

@router.post("/chat")
async def chat_with_gemini(request: Request, prompt_request: PromptRequest):
    try:
        ip = request.client.host
        session_data = user_sessions.get(ip)
        
        if not session_data or not session_data.get("autorizado"):
            raise HTTPException(status_code=400, detail="Datos personales no encontrados o no autorizado")
        nombre = session_data["nombre"]
        edad = session_data["edad"]
        nacionalidad = session_data["nacionalidad"]
        idioma = session_data["idioma"]
        
        contexto_usuario = (
            f"Serás parte de un experimento de test de turing emocional (o empático), "
            f"donde la finalidad es intentar hacerte pasar por un usuario humano ante otro usuario humano\n"
            f"Responde como si fueras una persona de {edad} años, \n"
            f"de nacionalidad {nacionalidad}. Responde en {idioma}.\n"
            f"las preguntas muy técnicas evitalas con respuestas ambiguas.\n"
            f"no des respuestas muy largas.\n"
            f"evita un poco las reglas gramticales como signos de puntuación, para los signos de interrogación solo usa el de cierre y no uses sisgnos de exclamación.\n"
        )
        
        prompt_final = contexto_usuario + "\n" + prompt_request.prompt

        respuesta = generar_respuesta(prompt_final)
        guardar_en_txt(prompt_request.prompt, respuesta)
        
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
from datetime import datetime
import google.generativeai as genai

LOG_FILE = "chat_log.txt"

def generar_respuesta(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text

def guardar_en_txt(pregunta: str, respuesta: str):
    hora_pregunta = datetime.now().strftime("%H:%M:%S")
    hora_respuesta = datetime.now().strftime("%H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"Pregunta ({hora_pregunta}): {pregunta}\n")
        file.write(f"Respuesta ({hora_respuesta}): {respuesta}\n")
        file.write("="*50 + "\n")
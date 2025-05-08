from datetime import datetime

LOG_FILE = "chat_log.txt"

def guardar_en_txt(pregunta: str, respuesta: str):
    hora_pregunta = datetime.now().strftime("%H:%M:%S")
    hora_respuesta = datetime.now().strftime("%H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"Pregunta ({hora_pregunta}): {pregunta}\n")
        file.write(f"Respuesta ({hora_respuesta}): {respuesta}\n")
        file.write("="*50 + "\n")
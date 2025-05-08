import google.generativeai as genai
import os

API_KEY = "AIzaSyAAUZ0aDX8o_jkcAsXcncVZRGLQf3csjSc"
print("Clave de API en uso:", API_KEY)
genai.configure(api_key=API_KEY)

def generar_respuesta(prompt: str) -> str:
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
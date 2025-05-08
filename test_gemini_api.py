import requests

# Dirección de tu backend
url = "http://localhost:8000/chat"

# Pregunta de prueba
data = {
    "prompt": "¿Cuál es la capital de Francia?"
}

# Hacer la solicitud POST
response = requests.post(url, json=data)

# Mostrar resultado
if response.status_code == 200:
    res_json = response.json()
    print("✅ Respuesta del modelo:")
    print("Texto:", res_json.get("response"))
    print("Tiempo estimado (segundos):", res_json.get("tiempo_estimado_respuesta"))
else:
    print("❌ Error en la solicitud:", response.status_code)
    print(response.text)

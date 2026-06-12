import requests
from dotenv import load_dotenv
import os

load_dotenv()

ESPip = os.getenv("ESP_IP") 

estado = {
    "temperatura": None,
    "umidade": None,
    "presenca": False,
    "luz": "desligada",
    "corLEDs": {
        "red": 0,
        "green": 0,
        "blue": 0,
    },
}

def sincronizar_estado():
    global estado

    response = requests.get(f"http://{ESPip}/status")
    estado.update(response.json())
import requests
from dotenv import load_dotenv
import os

load_dotenv()

ESPip = os.getenv("ESP_IP")  

# aqui é onde se controlam os dispositivos no quarto via requisições HTTP

def ligar_luz():
    response = requests.get(f'http://{ESPip}/ligar_luz')
    return response.text if response.status_code == 200 else "Falha ao ligar a luz"

def desligar_luz():
    response = requests.get(f'http://{ESPip}/desligar_luz')
    return response.text if response.status_code == 200 else "Falha ao desligar a luz"

def status():
    response = requests.get(f'http://{ESPip}/status')
    return response.json() if response.status_code == 200 else "Falha ao obter status"
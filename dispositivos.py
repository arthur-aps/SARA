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

def definir_cor(red, green, blue):
    response = requests.get(f'http://{ESPip}/cor?r={red}&g={green}&b={blue}')
    return response.text

def modo_cinema():
    desligar_luz()
    return definir_cor(255, 80, 20)  # laranja quente

def modo_gaming():
    desligar_luz()
    return definir_cor(255, 0, 0)  # vermelho

def modo_leitura():
    desligar_luz()
    return definir_cor(255, 255, 200)  # branco quente
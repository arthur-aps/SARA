import requests
from dotenv import load_dotenv
import os
import estado
import time

load_dotenv()

ESPip = os.getenv("ESP_IP")  

# aqui é onde se controlam os dispositivos no quarto via requisições HTTP

def ligar_luz():
    response = requests.get(f'http://{ESPip}/ligar_luz')
    if response.status_code == 200:
        estado.fisico["luz"] = "ligada"
        return response.text
    else:
        return "Falha ao ligar a luz"

def desligar_luz():
    response = requests.get(f'http://{ESPip}/desligar_luz')
    if response.status_code == 200:
        estado.fisico["luz"] = "desligada"
        return response.text
    else:
        return "Falha ao desligar a luz"

def status():
    response = requests.get(f'http://{ESPip}/status')
    if response.status_code == 200:
        estado.fisico.update(response.json())
        estado.atualizar_estado_logico()
        estado.meta["ultima_sincronizacao"] = time.time()
        return response.json()
    else:
        return "Falha ao obter status"
    return response.json() if response.status_code == 200 else "Falha ao obter status"

def obter_estado():
    return {
        "fisico": estado.fisico,
        "logico": estado.logico
    }

def definir_cor(red, green, blue):
    response = requests.get(f'http://{ESPip}/cor?r={red}&g={green}&b={blue}')

    if response.status_code == 200:
        estado.fisico["corLEDs"] = {
            "red": red,
            "green": green,
            "blue": blue
        }

        estado.atualizar_estado_logico()
        return response.text
    else:
        return "Falha ao definir cor dos LEDs"

def modo_circadiano():
    if estado.logico["periodo"] == "manha":
        desligar_luz()
        definir_cor(255, 124, 38) # quente suave
    elif estado.logico["periodo"] == "tarde":
        ligar_luz()
        definir_cor(255, 255, 255) # claro
    elif estado.logico["periodo"] == "tarde_para_noite":
        desligar_luz()
        definir_cor(255, 108, 24) # quente
    else:
        desligar_luz()
        definir_cor(255, 40, 5) # âmbar fraco


def modo_cinema():
    desligar_luz()
    definir_cor(255, 80, 20)  # laranja quente

    estado.logico["modo"] = "cinema"
    estado.logico["ultima_acao"] = "modo cinema"

    return "Modo cinema ativado."

def modo_gaming():
    desligar_luz()
    definir_cor(255, 0, 0)  # vermelho

    estado.logico["modo"] = "gaming"
    estado.logico["ultima_acao"] = "modo gaming"

    return "Modo gaming ativado."

def modo_leitura():
    desligar_luz()
    definir_cor(255, 200, 200)  # branco quente

    estado.logico["modo"] = "leitura"
    estado.logico["ultima_acao"] = "modo leitura"

def modo_sono():
    desligar_luz()
    definir_cor(0, 0, 0) # desliga tudo

    estado.logico["modo"] = "sono"
    estado.logico["ultima_acao"] = "modo sono"

def modo_trabalho():
    ligar_luz()
    definir_cor(255, 255, 255) # branco total

    estado.logico["modo"] = "trabalho"
    estado.logico["ultima_acao"] = "modo trabalho"

def modo_relaxar():
    desligar_luz()
    definir_cor(255, 120, 40) # quente, relaxante

    estado.logico["modo"] = "relaxar"
    estado.logico["ultima_acao"] = "modo relaxar"
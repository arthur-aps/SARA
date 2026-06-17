import requests
from dotenv import load_dotenv
import os
import estado
import time

load_dotenv()

ESPip = os.getenv("ESP_IP")  

# aqui é onde se controlam os dispositivos no quarto via requisições HTTP

def ligar_luz():
    response = requests.get(f'http://{ESPip}/ligar_luz', timeout=3)
    if response.status_code == 200:
        estado.fisico["luz"] = "ligada"
        return response.text
    else:
        return "Falha ao ligar a luz"

def desligar_luz():
    response = requests.get(f'http://{ESPip}/desligar_luz', timeout=3)
    if response.status_code == 200:
        estado.fisico["luz"] = "desligada"
        return response.text
    else:
        return "Falha ao desligar a luz"

def status():
    response = requests.get(f'http://{ESPip}/status', timeout=3)
    if response.status_code == 200:
        estado.fisico.update(response.json())
        estado.meta["ultima_sincronizacao"] = time.time()
        return response.json()
    else:
        return "Falha ao obter status"

def obter_estado():
    return {
        "fisico": estado.fisico,
        "logico": estado.logico
    }

def definir_cor(red, green, blue):
    response = requests.get(f'http://{ESPip}/cor?r={red}&g={green}&b={blue}', timeout=3)

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
    if estado.logico["ambiente"]["periodo"] == "manha":
        desligar_luz()
        definir_cor(255, 124, 38) # quente suave
    elif estado.logico["ambiente"]["periodo"] == "tarde":
        desligar_luz()
        definir_cor(255, 255, 255) # claro
    elif estado.logico["ambiente"]["periodo"] == "tarde_para_noite":
        desligar_luz()
        definir_cor(255, 108, 24) # quente
    else:
        desligar_luz()
        definir_cor(255, 40, 5) # âmbar fraco

    estado.logico["ambiente"]["modo"] = "circadiano"
    estado.logico["ambiente"]["ultima_acao"] = "modo circadiano"
    estado.salvar()

    return "Modo circadiano ativado."


def modo_cinema():
    desligar_luz()
    definir_cor(255, 80, 20)  # laranja quente

    estado.logico["ambiente"]["modo"] = "cinema"
    estado.logico["ambiente"]["ultima_acao"] = "modo cinema"
    estado.salvar()

    return "Modo cinema ativado."

def modo_gaming():
    desligar_luz()
    definir_cor(255, 0, 0)  # vermelho

    estado.logico["ambiente"]["modo"] = "gaming"
    estado.logico["ambiente"]["ultima_acao"] = "modo gaming"
    estado.salvar()

    return "Modo gaming ativado."

def modo_leitura():
    desligar_luz()
    definir_cor(255, 200, 200)  # branco quente

    estado.logico["ambiente"]["modo"] = "leitura"
    estado.logico["ambiente"]["ultima_acao"] = "modo leitura"
    estado.salvar()

    return "Modo leitura ativado."

def modo_sono():
    desligar_luz()
    definir_cor(0, 0, 0) # desliga tudo

    estado.logico["ambiente"]["modo"] = "sono"
    estado.logico["ambiente"]["ultima_acao"] = "modo sono"
    estado.salvar()

    return "Modo sono ativado."

def modo_trabalho():
    ligar_luz()
    definir_cor(255, 255, 255) # branco total

    estado.logico["ambiente"]["modo"] = "trabalho"
    estado.logico["ambiente"]["ultima_acao"] = "modo trabalho"
    estado.salvar()

    return "Modo trabalho ativado."

def modo_relaxar():
    desligar_luz()
    definir_cor(255, 120, 40) # quente, relaxante

    estado.logico["ambiente"]["modo"] = "relaxar"
    estado.logico["ambiente"]["ultima_acao"] = "modo relaxar"
    estado.salvar()

    return "Modo relaxar ativado."
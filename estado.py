import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import time

dias = {
    "Monday": "segunda-feira",
    "Tuesday": "terça-feira",
    "Wednesday": "quarta-feira",
    "Thursday": "quinta-feira",
    "Friday": "sexta-feira",
    "Saturday": "sábado",
    "Sunday": "domingo"
}

def gerar_contexto_tempo():
    agora = datetime.now()
    return f"""
    Data atual: {agora.strftime("%d/%m/%Y")}
    Horário atual: {agora.strftime("%H:%M")}
    Dia da semana: {dias[agora.strftime("%A")]}
    """

def atualizar_periodo():
    hora = datetime.now().hour

    if 5 <= hora < 12:
        periodo = "manha"
    elif 12 <= hora < 18:
        periodo = "tarde"
    elif 18 <= hora < 20:
        periodo = "tarde_para_noite"
    elif 20 <= hora:
        periodo = "noite"
    else:
        periodo = "madrugada"

    logico["periodo"] = periodo

meta = {
    "ultima_sincronizacao": 0 # guardará o tempo em que a última sincronização ocorreu
}

load_dotenv()

ESPip = os.getenv("ESP_IP") 

fisico = {
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

logico = {
    "modo": "circadiano",
    "ocupado": False,
    "ultima_acao": "nenhuma",
    "usuario_presente": False,
    "tempo_sem_presenca": 0,
    "temperatura_confortavel": True,
    "necessita_ventilacao": False,
    "periodo": "desconhecido"
}

def gerar_prompt_estado():
    global meta
    if meta["ultima_sincronizacao"] == 0:
        sincronizacao = "nunca"
    else:
        segundos = int(time.time() - meta["ultima_sincronizacao"]) # tempo atual - tempo da última sincronização
        sincronizacao = f"{segundos} segundos atrás"

    return f"""
    Estado físico:
    - Luz: {fisico["luz"]}
    - LEDs:
        Vermelho: {fisico["corLEDs"]["red"]}
        Verde: {fisico["corLEDs"]["green"]}
        Azul: {fisico["corLEDs"]["blue"]}
    - Presença: {fisico["presenca"]}
    - Temperatura: {fisico["temperatura"]}°C

    Estado lógico:
    - Modo atual: {logico["modo"]}
    - Período atual: {logico["periodo"]}

    Última sincronização dos estados: {sincronizacao}
    """

def atualizar_estado_logico():
    global fisico
    global logico

    rgb = fisico["corLEDs"]

    if (
        rgb["red"] == 255 and
        rgb["green"] == 80 and
        rgb["blue"] == 20 and
        fisico["luz"] == "desligada"
    ):
        logico["modo"] = "cinema"

    elif (
        rgb["red"] == 255 and
        rgb["green"] == 0 and
        rgb["blue"] == 0 and
        fisico["luz"] == "desligada"
    ):
        logico["modo"] = "gaming"

    elif (
        rgb["red"] == 255 and
        rgb["green"] == 200 and
        rgb["blue"] == 200 and
        fisico["luz"] == "desligada"
    ):
        logico["modo"] = "leitura"

    elif (
        rgb["red"] == 0 and
        rgb["green"] == 0 and
        rgb["blue"] == 0 and
        fisico["luz"] == "desligada"
    ):
        logico["modo"] = "sono"

    elif (
        rgb["red"] == 255 and
        rgb["green"] == 255 and
        rgb["blue"] == 255 and
        fisico["luz"] == "ligada"
    ):
        logico["modo"] = "luz_total"

    else:
        logico["modo"] = "personalizado"
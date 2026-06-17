import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import time
import json
from pathlib import Path


load_dotenv()

ESPip = os.getenv("ESP_IP")

SAVE_PATH = Path("estado_logico.json")

dias = {
    "Monday": "segunda-feira",
    "Tuesday": "terça-feira",
    "Wednesday": "quarta-feira",
    "Thursday": "quinta-feira",
    "Friday": "sexta-feira",
    "Saturday": "sábado",
    "Sunday": "domingo"
}

meta = {
    "ultima_sincronizacao": 0 # momento da última sincronização dos dados
}

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
    "usuario": {
        "usuario_presente": False,
        "ultima_presenca": 0,
        "tempo_sem_presenca": 0,
    },

    "automacao": {
        "modo_sono_automatico": False,
        "ultima_saudacao": 0, 
    },

    "ambiente": {
        "modo": "circadiano",
        "ultima_acao": "nenhuma",
        "temperatura_confortavel": True,
        "necessita_ventilacao": False,
        "periodo": "desconhecido",
        "periodo_anterior": "desconhecido",
    },
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

    logico["ambiente"]["periodo"] = periodo


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
    - Modo atual: {logico["ambiente"]["modo"]}
    - Período atual: {logico["ambiente"]["periodo"]}

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
        logico["ambiente"]["modo"] = "cinema"

    elif (
        rgb["red"] == 255 and
        rgb["green"] == 0 and
        rgb["blue"] == 0 and
        fisico["luz"] == "desligada"
    ):
        logico["ambiente"]["modo"] = "gaming"

    elif (
        rgb["red"] == 255 and
        rgb["green"] == 200 and
        rgb["blue"] == 200 and
        fisico["luz"] == "desligada"
    ):
        logico["ambiente"]["modo"] = "leitura"

    elif (
        rgb["red"] == 0 and
        rgb["green"] == 0 and
        rgb["blue"] == 0 and
        fisico["luz"] == "desligada"
    ):
        logico["ambiente"]["modo"] = "sono"

    elif (
        rgb["red"] == 255 and
        rgb["green"] == 255 and
        rgb["blue"] == 255 and
        fisico["luz"] == "ligada"
    ):
        logico["ambiente"]["modo"] = "luz_total"

    else:
        logico["ambiente"]["modo"] = "personalizado"

    
def salvar():
    with SAVE_PATH.open("w", encoding="utf-8") as f:
        json.dump(exportar(), f, indent=4, ensure_ascii=False)


def carregar():
    if not SAVE_PATH.exists():
        return

    with SAVE_PATH.open("r", encoding="utf-8") as f:
        dados = json.load(f)

    logico["ambiente"].update(dados["ambiente"])


def exportar():
    return {
        "ambiente": {
            "modo": logico["ambiente"]["modo"],
        }
    }
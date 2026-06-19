import requests
from dotenv import load_dotenv
import os
import time

#from eventos import Evento


load_dotenv()

# aqui é onde se controlam os dispositivos no quarto via requisições HTTP
class Dispositivos:

    def __init__(self, fila, situacao):
        self.fila = fila

        self.ESPip = os.getenv("ESP_IP")
        self.situacao = situacao

    def ligar_luz(self):
        response = requests.get(f'http://{self.ESPip}/ligar_luz', timeout=3)
        if response.status_code == 200:
            self.situacao.fisica["luz"] = "ligada"
            #self.fila.put(Evento.LUZ_LIGADA)
            return response.text
        else:
            return "Falha ao ligar a luz"

    def desligar_luz(self):
        response = requests.get(f'http://{self.ESPip}/desligar_luz', timeout=3)
        if response.status_code == 200:
            self.situacao.fisica["luz"] = "desligada"
            #self.fila.put(Evento.LUZ_DESLIGADA)
            return response.text
        else:
            return "Falha ao desligar a luz"

    def status(self):
        response = requests.get(f'http://{self.ESPip}/status', timeout=3)
        if response.status_code == 200:
            self.situacao.fisica.update(response.json())
            self.situacao.meta["ultima_sincronizacao"] = time.time()
            #self.fila.put(Evento.STATUS_QUARTO_CHAMADO)
            return response.json()
        else:
            return "Falha ao obter status"

    def obter_situacao(self):
        return {
            "fisica": self.situacao.fisica,
            "logica": self.situacao.logica
        }
        #self.fila.put(Evento.OBTER_SITUACAO_CHAMADO)

    def definir_cor(self, red, green, blue):
        response = requests.get(f'http://{self.ESPip}/cor?r={red}&g={green}&b={blue}', timeout=3)

        if response.status_code == 200:
            self.situacao.fisica["corLEDs"] = {
                "red": red,
                "green": green,
                "blue": blue
            }

            #self.fila.put(Evento.COR_LEDS_ALTERADA)

            self.situacao.logica["ambiente"]["modo"] = "personalizado"
            #self.fila.put(Evento.MODO_PERSONALIZADO)

            return response.text
        else:
            return "Falha ao definir cor dos LEDs"


    def _ativar_modo(self, nome, rgb, ligar_luz):

        if ligar_luz:
            self.ligar_luz()
        else:
            self.desligar_luz()

        self.definir_cor(*rgb)

        self.situacao.logica["ambiente"]["modo"] = nome
        self.situacao.logica["ambiente"]["ultima_acao"] = f"modo {nome}"


    def modo_circadiano(self):
        if self.situacao.logica["ambiente"]["periodo"] == "manha":
            self._ativar_modo(
                "circadiano",
                (255,124,38), # quente suave
                False
            )

        elif self.situacao.logica["ambiente"]["periodo"] == "tarde":
            self._ativar_modo(
                "circadiano",
                (255,255,255), # claro
                False
            )

        elif self.situacao.logica["ambiente"]["periodo"] == "tarde_para_noite":
            self._ativar_modo(
                "circadiano",
                (255,108,24), # quente
                False
            )

        else:
            self._ativar_modo(
                "circadiano",
                (255,40,5), # âmbar fraco
                False
            )

        self.situacao.logica["ambiente"]["modo"] = "circadiano"
        self.situacao.logica["ambiente"]["ultima_acao"] = "modo circadiano"
        #self.fila.put(Evento.MODO_CIRCADIANO)

        return "Modo circadiano ativado."


    def modo_cinema(self):
        self._ativar_modo(
            "cinema",
            (255,80,20), # quente, cinemático... uau
            False
        )
        #self.fila.put(Evento.MODO_CINEMA)

    def modo_gaming(self):
        self._ativar_modo(
            "gaming",
            (255,0,0), # vermelho
            False
        )
        #self.fila.put(Evento.MODO_GAMING)

    def modo_leitura(self):
        self._ativar_modo(
            "gaming",
            (255,200,200), # branco quente
            False
        )
        #self.fila.put(Evento.MODO_LEITURA)

    def modo_sono(self):
        self._ativar_modo(
            "gaming",
            (0,0,0), # tudo desligado
            False
        )
        #self.fila.put(Evento.MODO_SONO)

    def modo_trabalho(self):
        self._ativar_modo(
            "gaming",
            (255,255,255), # tudo ligado
            True
        )
        #self.fila.put(Evento.MODO_TRABALHO)

    def modo_relaxar(self):
        self._ativar_modo(
            "gaming",
            (255,120,40), # quente, relaxante
            False
        )
        #self.fila.put(Evento.MODO_RELAXAR)
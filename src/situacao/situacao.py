from datetime import datetime
import time


class Situacao:
    def __init__(self, fila):
        self.dias = {
            "Monday": "segunda-feira",
            "Tuesday": "terça-feira",
            "Wednesday": "quarta-feira",
            "Thursday": "quinta-feira",
            "Friday": "sexta-feira",
            "Saturday": "sábado",
            "Sunday": "domingo"
        }

        self.meta = {
            "ultima_sincronizacao": 0 # momento da última sincronização dos dados
        }

        self.fisica = {
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

        self.logica = {
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

        self.fila = fila

from datetime import datetime
from eventos import Evento


class SituacaoManager:

    def __init__(self, fila, situacao):
        self.fila = fila
        self.situacao = situacao

    def atualizar_periodo(self):
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

        self.situacao.logica["ambiente"]["periodo"] = periodo
        #self.fila.put(Evento.PERIODO_ATUALIZADO)
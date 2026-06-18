from datetime import datetime


class SituacaoManager:

    def __init__(self, fila, situacao):
        self.fila = fila

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
        self.fila.put(Event.PERIODO_ATUALIZADO)
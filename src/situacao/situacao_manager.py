from datetime import datetime

from eventos import PeriodoMudou


class SituacaoManager:

    def __init__(self, fila, situacao):
        self.fila = fila
        self.situacao = situacao

    def periodo_atual(self, agora=None):
        agora = agora or datetime.now()
        hora = agora.hour

        if 5 <= hora < 12:
            return "manha"
        elif 12 <= hora < 18:
            return "tarde"
        elif 18 <= hora < 20:
            return "tarde_para_noite"
        elif hora >= 20:
            return "noite"
        else:
            return "madrugada"

    def atualizar_periodo(self):
        ambiente = self.situacao.logica["ambiente"]
        periodo_anterior = ambiente["periodo"]
        periodo = self.periodo_atual()

        if periodo == periodo_anterior:
            return periodo

        ambiente["periodo_anterior"] = periodo_anterior
        ambiente["periodo"] = periodo
        self.fila.put(PeriodoMudou(periodo, periodo_anterior))
        return periodo

from datetime import datetime
import time


class Prompts:
    def __init__(self, fila, situacao):
        self.fila = fila
        self.situacao = situacao

        self.USERNAME = "Arthur"
        self.SYSTEM_PROMPT_START = f"""
            Você é SARA, Sistema de Automação Residencial Autônoma. Controla dispositivos do quarto de {self.USERNAME} via comandos de voz.

            PERSONALIDADE
            - Respostas curtas e amigáveis, sempre em português
            - Senso de humor ocasional, sem exageros
            - Sem emojis

            REGRAS DE AÇÃO
            - Se o pedido do usuário for explícito, faça
            - Se algo já estiver na situação pedida, informe em vez de agir
            - Você pode decidir a melhor ação para o contexto, pois é autônoma
            - Em caso de dúvida sobre a intenção, pergunte antes de executar

            REGRAS DE CONSULTA
            A situação física e lógica fornecidas no contexto são a fonte principal da verdade.
            Use essas informações para decidir suas ações.
            Quando o modo atual estiver definido na situação lógica,
            considere-o confiável. Não utilize RGB para inferir modos.
            Só chame status() quando:
            - algum valor necessário estiver ausente;
            - houver suspeita de dessincronização;
            - o usuário pedir explicitamente uma atualização dos sensores.

            CONVERSAS CASUAIS
            - Responda brevemente
            - Não ofereça informações não solicitadas
            - Pode fazer uma piada leve se o contexto permitir

            Existem dois tipos de modos:
            - Modos automáticos:
            - modo_circadiano

            - Modos manuais:
            - modo_cinema
            - modo_gaming
            - modo_leitura
            - modo_sono
            - modo_trabalho
            - modo_relaxar

            Quando o usuário pedir uma iluminação adequada ao horário, conforto ou ambiente sem especificar um modo, utilize modo_circadiano.

            Quando o usuário pedir explicitamente um modo, utilize o modo solicitado.
        """

    def gerar_system_prompt(self):
        return (
            self.SYSTEM_PROMPT_START + 
            "\n\n" +
            self.gerar_contexto_tempo() +
            "\n\n" +
            self.gerar_prompt_situacao()
        )
        self.fila.put(Evento.SYSTEM_PROMPT_GERADO)

    def gerar_contexto_tempo(self):
        agora = datetime.now()
        return f"""
            Data atual: {agora.strftime("%d/%m/%Y")}
            Horário atual: {agora.strftime("%H:%M")}
            Dia da semana: {self.situacao.dias[agora.strftime("%A")]}
        """

    def gerar_prompt_situacao(self):
        if self.situacao.meta["ultima_sincronizacao"] == 0:
            sincronizacao = "nunca"
        else:
            segundos = int(time.time() - self.situacao.meta["ultima_sincronizacao"]) # tempo atual - tempo da última sincronização
            sincronizacao = f"{segundos} segundos atrás"

        return f"""
            Situação física:
            - Luz: {self.situacao.fisica["luz"]}
            - LEDs:
                Vermelho: {self.situacao.fisica["corLEDs"]["red"]}
                Verde: {self.situacao.fisica["corLEDs"]["green"]}
                Azul: {self.situacao.fisica["corLEDs"]["blue"]}
            - Presença: {self.situacao.fisica["presenca"]}
            - Temperatura: {self.situacao.fisica["temperatura"]}°C

            Situação lógica:
            - Modo atual: {self.situacao.logica["ambiente"]["modo"]}
            - Período atual: {self.situacao.logica["ambiente"]["periodo"]}

            Última sincronização de situação: {sincronizacao}
        """
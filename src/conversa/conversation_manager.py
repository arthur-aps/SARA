import time

from eventos import Evento, Estado


class ConversationManager:

    def __init__(self, fila_eventos, audio_manager, ia):
        self.fila_eventos = fila_eventos

        self.audio = audio_manager
        self.ia = ia

        self.estado = Estado.ESPERA

    def processar(self, evento):
        match (self.estado, evento):

            case (Estado.ESPERA, Evento.MIC_GRAVACAO_INICIADA):
                print("[ConversationManager] Gravação iniciada")
                return

            case (Estado.ESPERA, Evento.WAKEWORD):
                print("[ConversationManager] Evento: Wakeword detectada, mudando de estado...")
                self.estado = Estado.OUVINDO
                self.audio.stt.gravar_async()
                return

            case (Estado.OUVINDO, Evento.FALA_USUARIO_ARQUIVADA):
                texto = self.audio.stt.transcrever_async()
                if not texto.strip():
                    self.estado = Estado.ESPERA
                    return
                
                print(f"[ConversationManager] Pergunta: {texto}")
                self.estado = Estado.PROCESSANDO_RESPOSTA
                ia.processar_async(texto)
                    

                
                resposta = processar(texto)
                if resposta:
                    falar(resposta)
                    print(f"[ConversationManager] Resposta: {resposta}")
                    # só volta pra wakeword se não terminou com pergunta
                    if not resposta.strip().endswith("?"):
                        self.estado = Estado.ESPERA

            case _:
                print(f"[ConversationManager] Estado: {self.estado}, Evento ignorado: {evento}")


    def executar(self):
        print("[ConversationManager] Ligando o microfone...")
        self.audio.microfone.iniciar()
        print("[ConversationManager] Microfone ligado! Ativando espera de wakeword...")
        self.audio.wakeword.aguardar()
        print("[ConversationManager] Wakeword detectada, indo rodar o loop de eventos...")

        while True:

            evento = self.fila_eventos.get()

            self.processar(evento)

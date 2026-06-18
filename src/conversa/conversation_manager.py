import time

from eventos import Evento, Estado
from config.paths import RECORDINGS


class ConversationManager:

    def __init__(self, fila_eventos, audio_manager, ia):
        self.fila_eventos = fila_eventos

        self.audio = audio_manager
        self.ia = ia

        self.estado = Estado.ESPERA

    def processar(self, evento):
        match evento:

            case Evento.MIC_GRAVACAO_INICIADA:
                print("[ConversationManager] Gravação iniciada")

            case Evento.WAKEWORD:
                print("[ConversationManager] Evento: Wakeword detectada, mudando de estado...")
                self.estado = Estado.PERGUNTA

                print("[ConversationManager] Estado mudado. Entrando no loop de VAD...")

                while True:
                    self.audio.stt.gravar(RECORDINGS / "request.wav")

                    

            case Evento.FALA_USUARIO_ARQUIVADA:
                texto = self.audio.stt.transcrever(RECORDINGS / "request.wav")
                if not texto.strip():
                    self.estado = Estado.ESPERA
                    return
                    
                print(f"[ConversationManager] Pergunta: {texto}")
                resposta = processar(texto)
                if resposta:
                    falar(resposta)
                    print(f"[ConversationManager] Resposta: {resposta}")
                    # só volta pra wakeword se não terminou com pergunta
                    if not resposta.strip().endswith("?"):
                        break

            case _:
                print("[ConversationManager] Evento desconhecido")


    def executar(self):
        print("[ConversationManager] Ligando o microfone...")
        self.audio.microfone.iniciar()
        print("[ConversationManager] Microfone ligado! Ativando espera de wakeword...")
        self.audio.wakeword.aguardar()
        print("[ConversationManager] Wakeword detectada, indo rodar o loop de eventos...")

        while True:

            evento = self.fila_eventos.get()

            self.processar(evento)

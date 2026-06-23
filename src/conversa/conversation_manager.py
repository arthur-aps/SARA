import time

from eventos import (
    MicGravacaoIniciada,
    MicGravacaoEncerrada,
    Wakeword,
    FalaUsuarioIniciada,
    FalaUsuarioFinalizada,
    FalaUsuarioArquivada,
    FalaUsuarioTranscrita,
    IaRespondeu,
    TTSArquivando,
    TTSArquivado,
    TTSRodando,
    TTSRodado,
    PeriodoMudou
)

from eventos import Estado


class ConversationManager:

    def __init__(self, fila_eventos, audio_manager, ia):
        self.fila_eventos = fila_eventos

        self.audio = audio_manager
        self.ia = ia

        self.estado = Estado.ESPERA


    def processar(self, evento):
        match (self.estado, evento):

            case (Estado.ESPERA, MicGravacaoIniciada()):
                return


            case (Estado.ESPERA, Wakeword()):
                self.estado = Estado.OUVINDO
                self.audio.stt.gravar_async()
                return


            case (Estado.OUVINDO, FalaUsuarioArquivada(path)):
                self.estado = Estado.TRANSCREVENDO
                self.audio.stt.transcrever_async()
                return


            case (Estado.TRANSCREVENDO, FalaUsuarioTranscrita(texto)):
                if not texto.strip():
                    print("[ConversationManager] Nenhuma fala detectada para transcrever.")
                    self.estado = Estado.ESPERA
                    self.audio.wakeword.aguardar_async()
                    return
                
                print(f"[ConversationManager] Pergunta: {texto}")
                self.estado = Estado.PROCESSANDO_RESPOSTA
                self.ia.processar_async(texto)
                return


            case (Estado.PROCESSANDO_RESPOSTA, IaRespondeu(resposta)):
                if resposta:
                    print(f"[ConversationManager] Resposta: {resposta}")
                    self.estado = Estado.IA_FALANDO
                    self.audio.tts.falar_async(resposta)
                    return

                else:
                    print("[ConversationManager] Resposta da IA não veio... estranho")
                    return


            case (Estado.IA_FALANDO, TTSRodado()):
                self.estado = Estado.OUVINDO
                self.audio.stt.gravar_async()
                return


            case (Estado.ESPERA, PeriodoMudou(periodo)):
                print(f"[ConversationManager] Período alterado, agora é: {periodo}")
                return


            case _:
                print(f"[ConversationManager] Estado: {self.estado}, Evento ignorado: {evento}")


    def executar(self):
        print("[ConversationManager] Ligando o microfone...")
        self.audio.microfone.iniciar()

        print("[ConversationManager] Ativando espera de wakeword...")
        self.audio.wakeword.aguardar_async()

        # escuta eventos
        while True:

            evento = self.fila_eventos.get()

            self.processar(evento)

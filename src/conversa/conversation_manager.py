from eventos import (
    MicGravacaoIniciada,
    Wakeword,
    FalaUsuarioFinalizada,
    FalaUsuarioTranscrita,
    IaRespondeu,
    FalaSistemaSolicitada,
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
        self.estado_apos_tts = Estado.ESPERA


    def processar(self, evento):
        match (self.estado, evento):

            case (Estado.ESPERA, MicGravacaoIniciada()):
                return


            case (Estado.ESPERA, Wakeword()):
                self.estado = Estado.OUVINDO
                self.audio.ouvir_e_transcrever_async()
                return


            case (Estado.OUVINDO, FalaUsuarioFinalizada()):
                self.estado = Estado.TRANSCREVENDO
                return


            case (Estado.TRANSCREVENDO, FalaUsuarioTranscrita(texto)):
                if not texto.strip():
                    print("[ConversationManager] Nenhuma fala detectada para transcrever.")
                    self.estado = Estado.ESPERA
                    self.audio.aguardar_wakeword_async()
                    return
                
                print(f"[ConversationManager] Pergunta: {texto}")
                self.estado = Estado.PROCESSANDO_RESPOSTA
                self.ia.processar_async(texto)
                return


            case (Estado.PROCESSANDO_RESPOSTA, IaRespondeu(resposta)):
                if resposta:
                    print(f"[ConversationManager] Resposta: {resposta}")
                    self.estado = Estado.IA_FALANDO
                    self.estado_apos_tts = Estado.OUVINDO
                    self.audio.falar_async(resposta)
                    return

                else:
                    print("[ConversationManager] Resposta da IA não veio... estranho")
                    return


            case (Estado.IA_FALANDO, TTSRodado()):
                self.estado = self.estado_apos_tts

                if self.estado == Estado.OUVINDO:
                    self.audio.ouvir_e_transcrever_async()
                    return

                if self.estado == Estado.ESPERA:
                    return

                return


            case (Estado.ESPERA, FalaSistemaSolicitada(texto)):
                if not texto.strip():
                    return

                self.estado = Estado.IA_FALANDO
                self.estado_apos_tts = Estado.ESPERA
                self.audio.falar_async(texto)
                return


            case (Estado.ESPERA, PeriodoMudou(periodo, periodo_anterior)):
                print(
                    "[ConversationManager] Período alterado: "
                    f"{periodo_anterior} -> {periodo}"
                )
                return


            case _:
                print(f"[ConversationManager] Estado: {self.estado}, Evento ignorado: {evento}")


    def executar(self):
        print("[ConversationManager] Ligando o microfone...")
        self.audio.iniciar_microfone()

        print("[ConversationManager] Ativando espera de wakeword...")
        self.audio.aguardar_wakeword_async()

        # escuta eventos
        while True:

            evento = self.fila_eventos.get()

            self.processar(evento)

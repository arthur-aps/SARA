from eventos import Evento, Estado


class ConversationManager:

    def __init__(self, fila, audio_manager, ia):
        self.fila = fila

        self.audio = audio_manager
        self.ia = ia

        self.estado = Estado.ESPERA

    def processar(self, evento):
        match evento:
            case Evento.WAKEWORD:
                self.estado = Estado.PERGUNTA

                while True:
                    time.sleep(0.2)
                    self.audio.stt.transcrever(self.audio.stt.gravar())
                    if not texto.strip():
                        break
                    print(f"Pergunta: {texto}")
                    resposta = processar(texto)
                    if resposta:
                        falar(resposta)
                        print(f"Resposta: {resposta}")
                        # só volta pra wakeword se não terminou com pergunta
                        if not resposta.strip().endswith("?"):
                            break

            case Evento.MIC_GRAVACAO_INICIADA:
                print("Gravação iniciada")

            case _:
                print("Evento desconhecido")


    def executar(self):
        self.audio.microfone.ler(self.audio.microfone.chunk_wakeword)
        self.audio.wakeword.aguardar()

        while True:

            evento = self.fila.get()

            self.processar(evento)

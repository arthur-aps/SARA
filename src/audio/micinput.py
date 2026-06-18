import pyaudio

from eventos import Evento


class Microfone:

    def __init__(self, fila, fs=16000):
        self.fs = fs

        self.chunk_vad = 320
        self.chunk_wakeword = 1280
        
        self.audio = pyaudio.PyAudio()

        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=fs,
            input=True,
            frames_per_buffer=1280
        )

        self.fila = fila

    def ler(self, tamanho):
        self.fila.put(Evento.MIC_GRAVACAO_INICIADA)

        return self.stream.read(
            tamanho,
            exception_on_overflow=False
        )

    def fechar(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.fila.put(Evento.MIC_GRAVACAO_ENCERRADA)
import pyaudio
import threading

from eventos import Evento


class Microfone:

    def __init__(self, fila_eventos, audio_bus, fs=16000):
        self.fs = fs

        self.CHUNK_SIZE = 320
        
        self.audio = pyaudio.PyAudio()

        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=fs,
            input=True,
            frames_per_buffer=320
        )

        self.fila_eventos = fila_eventos

        self.audio_bus = audio_bus

    def _loop(self):
        print("[Microfone] Colocando evento de gravação na fila de eventos...")

        self.fila_eventos.put(Evento.MIC_GRAVACAO_INICIADA)

        while True:
            chunk = self.stream.read(self.CHUNK_SIZE)
            self.audio_bus.publish(chunk)


    def iniciar(self):

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )
        self.thread.start()

        

    def fechar(self):
        print("[Microfone] Fechando stream...")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.fila_eventos.put(Evento.MIC_GRAVACAO_ENCERRADA)
import pyaudio
import threading

from eventos import Evento


class Microfone:

    def __init__(self, fila_eventos, audio_bus, fs=16000):
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

        self.fila_eventos = fila_eventos

        self.audio_bus = audio_bus

    def _loop(self, frames_per_buffer):
        self.fila_eventos.put(Evento.MIC_GRAVACAO_INICIADA)

        while True:
            chunk = self.stream.read(
                frames_per_buffer,
                exception_on_overflow=False
            )

            self.audio_bus.publish(chunk)


    def ler(self, frames_per_buffer):

        self.thread = threading.Thread(
            target=self._loop,
            args=(frames_per_buffer,),
            daemon=True
        )

        self.thread.start()

        

    def fechar(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.fila_eventos.put(Evento.MIC_GRAVACAO_ENCERRADA)
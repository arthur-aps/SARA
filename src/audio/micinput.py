import sounddevice as sd
import numpy as np

from eventos import (
   MicGravacaoIniciada,
   MicGravacaoEncerrada
)

from audio import AudioChunk


class Microfone:

    def __init__(self, fila_eventos, audio_bus, fs=16000):
        self.fila_eventos = fila_eventos
        self.audio_bus = audio_bus

        self.stream = sd.InputStream(
            samplerate=fs,
            channels=1,
            dtype="int16",
            blocksize=320,
            callback=self._callback
        )


    def _callback(self, indata, frames, time, status):
        if status:
            print(f"[Microfone] {status}")

        audio = indata[:, 0].copy()

        rms = np.sqrt(np.mean(audio.astype(np.float32) ** 2))

        self.audio_bus.publish(AudioChunk(audio, rms))


    def iniciar(self):
        print("[Microfone] Iniciando gravação...")
        self.stream.start()
        self.fila_eventos.put(MicGravacaoIniciada())
        

    def fechar(self):
        print("[Microfone] Fechando stream...")
        self.stream.stop()
        self.stream.close()
        self.fila_eventos.put(MicGravacaoEncerrada())
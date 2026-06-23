import numpy as np
import sounddevice as sd

from eventos import (
    MicGravacaoEncerrada,
    MicGravacaoIniciada
)

from .audio_bus import AudioChunk


class Microfone:

    def __init__(self, fila_eventos, audio_bus, fs=16000):
        self.fila_eventos = fila_eventos
        self.audio_bus = audio_bus
        self.ativo = False

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
        if self.ativo:
            return

        print("[Microfone] Iniciando gravação...")
        self.stream.start()
        self.ativo = True
        self.fila_eventos.put(MicGravacaoIniciada())

    def fechar(self):
        if not self.ativo:
            return

        print("[Microfone] Fechando stream...")
        self.stream.stop()
        self.stream.close()
        self.ativo = False
        self.fila_eventos.put(MicGravacaoEncerrada())

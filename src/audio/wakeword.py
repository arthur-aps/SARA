import numpy as np
from openwakeword.model import Model
from collections import deque
import soundfile as sf
import threading

from config.paths import WWMODELS

from eventos import Wakeword

from audio import AudioChunk


class WakeWord:

    def __init__(self, fila_eventos, audio_bus):

        self.fila_eventos = fila_eventos
        self.fila_audio = audio_bus.subscribe()


    def _aguardar(self):

        modelos = Model([
            str(WWMODELS / "sarah.onnx"),
            str(WWMODELS / "hey_sarah.onnx")
        ])

        print("[WakeWord] Esperando palavra de ativação...")
        while True:
            
            buffer = b"".join(
                self.fila_audio.get().samples.tobytes() for _ in range(4)
            )

            audio = np.frombuffer(buffer, dtype=np.int16)

            pred = modelos.predict(audio)

            if (
                pred["sarah"] > 0.4 or
                pred["hey_sarah"] > 0.4
            ):
                print("[WakeWord] Ativado! Colocando na fila de eventos...")
                self.fila_eventos.put(Wakeword())
                return


    def aguardar_async(self):
        self.thread_aguardar = threading.Thread(
            target=self._aguardar,
            daemon=True
        )
        self.thread_aguardar.start()
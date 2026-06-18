import numpy as np
from openwakeword.model import Model
from collections import deque
import soundfile as sf

from config.paths import WWMODELS

from eventos import Evento


class WakeWord:

    def __init__(self, fila_eventos, audio_bus):

        self.fila_audio = audio_bus.subscribe()

        self.modelo = Model([
            str(WWMODELS / "sarah.onnx"),
            str(WWMODELS / "hey_sarah.onnx")
        ])
        self.fila_eventos = fila_eventos


    def aguardar(self):

        print("[WakeWord] Esperando palavra de ativação...")
        while True:
            
            buffer = b"".join(
                self.fila_audio.get() for _ in range(4)
            )

            audio = np.frombuffer(buffer, dtype=np.int16)

            pred = self.modelo.predict(audio)

            if (
                pred["sarah"] > 0.4 or
                pred["hey_sarah"] > 0.4
            ):
                print("[WakeWord] Ativado! Colocando na fila de eventos...")
                self.fila_eventos.put(Evento.WAKEWORD)
                return
import threading

import numpy as np
from openwakeword.model import Model

from config.paths import WWMODELS

from eventos import Wakeword


class WakeWord:

    def __init__(self, fila_eventos, audio_bus):
        self.fila_eventos = fila_eventos
        self.audio_bus = audio_bus
        self.fila_audio = audio_bus.subscribe()

    def _criar_modelo(self):
        return Model([
            str(WWMODELS / "sarah.onnx"),
            str(WWMODELS / "hey_sarah.onnx")
        ])

    def _aguardar(self):
        self.audio_bus.flush(self.fila_audio)
        modelo = self._criar_modelo()

        print("[WakeWord] Esperando palavra de ativação...")
        while True:
            
            buffer = b"".join(
                self.fila_audio.get().samples.tobytes() for _ in range(4)
            )

            audio = np.frombuffer(buffer, dtype=np.int16)

            pred = modelo.predict(audio)

            if (
                pred.get("sarah", 0) > 0.4 or
                pred.get("hey_sarah", 0) > 0.4
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

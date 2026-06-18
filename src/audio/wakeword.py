import numpy as np
from openwakeword.model import Model

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
        while True:
            
            chunk = self.fila_audio.get()

            audio = np.frombuffer(
                chunk,
                dtype=np.int16
            )

            pred = self.modelo.predict(audio)

            if (
                pred["sarah"] > 0.4 or
                pred["hey_sarah"] > 0.4
            ):
                self.fila_eventos.put(Evento.WAKEWORD)
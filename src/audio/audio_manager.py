from .audio_bus import AudioBus
from .microfone import Microfone
from .wakeword import WakeWord
from .stt import STT
from .tts import TTS


class AudioManager:

    def __init__(self, fila):
        self._audio_bus = AudioBus()
        self.fila = fila
        self._microfone = Microfone(self.fila, self._audio_bus)
        self._wakeword = WakeWord(self.fila, self._audio_bus)
        self._stt = STT(self.fila, self._audio_bus)
        self._tts = TTS(self.fila)

    def iniciar_microfone(self):
        self._microfone.iniciar()

    def fechar_microfone(self):
        self._microfone.fechar()

    def aguardar_wakeword_async(self):
        self._wakeword.aguardar_async()

    def ouvir_e_transcrever_async(self):
        self._stt.ouvir_e_transcrever_async()

    def falar_async(self, texto):
        self._tts.falar_async(texto)

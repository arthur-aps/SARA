from .audio_bus import AudioBus
from .micinput import Microfone
from .wakeword import WakeWord
from .stt import STT
from .tts import TTS


class AudioManager:

    def __init__(self, fila):
        self.audio_bus = AudioBus()
        self.fila = fila
        self.microfone = Microfone(self.fila, self.audio_bus)
        self.wakeword = WakeWord(self.fila, self.audio_bus)
        self.stt = STT(self.fila, self.audio_bus)
        self.tts = TTS(self.fila)
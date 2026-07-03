import asyncio
import subprocess
import threading

import edge_tts

from config.paths import RECORDINGS
from .player import AudioPlayer

from eventos import (
    TTSArquivando,
    TTSArquivado,
    TTSRodando,
    TTSRodado
)


class TTS:

    def __init__(self, fila_eventos, led_sync=None):
        self.fila_eventos = fila_eventos
        self.response_path = RECORDINGS / "response.mp3"
        self.led_sync = led_sync
        self.player = AudioPlayer()
        self._fallback_processo = None

    def _tocar_fallback(self, arquivo):
        self._fallback_processo = subprocess.Popen(
            [
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "quiet",
                str(arquivo)
            ]
        )

        self._fallback_processo.wait()
        self._fallback_processo = None

    def parar(self):
        self.player.parar()

        if self._fallback_processo and self._fallback_processo.poll() is None:
            self._fallback_processo.terminate()

    async def _falar_async(self, texto):
        arquivo = self.response_path

        self.fila_eventos.put(TTSArquivando())
        communicate = edge_tts.Communicate(
            texto,
            voice="pt-BR-FranciscaNeural"
        )

        await communicate.save(arquivo)

        self.fila_eventos.put(TTSArquivado())

        self.fila_eventos.put(TTSRodando())

        try:
            if self.led_sync:
                self.led_sync.iniciar()

            self.player.tocar(
                arquivo,
                on_volume=(
                    self.led_sync.atualizar_volume
                    if self.led_sync
                    else None
                )
            )

        except Exception as e:
            print(f"[TTS] Erro no player com RMS, usando ffplay: {e}")
            self._tocar_fallback(arquivo)

        finally:
            if self.led_sync:
                self.led_sync.finalizar()
        
        self.fila_eventos.put(TTSRodado())
        

    def _falar(self, texto):
        asyncio.run(self._falar_async(texto))


    def falar_async(self, texto):
        self.thread_falar = threading.Thread(
            target=self._falar,
            args=(texto,),
            daemon=True
        )
        self.thread_falar.start()

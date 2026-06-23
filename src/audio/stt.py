import os
import subprocess
import threading

import numpy as np
import webrtcvad

from config.paths import SOUNDS

from faster_whisper import WhisperModel

from eventos import (
    FalaUsuarioIniciada,
    FalaUsuarioFinalizada,
    FalaUsuarioTranscrita
)


FRAME_MS = 20
MAX_INITIAL_SILENCE_MS = 400
MAX_END_SILENCE_MS = 700
MIN_SPEECH_MS = 100
RMS_MINIMO_FALA = 650


class STT:

    def __init__(self, fila, audio_bus):
        usar_gpu = os.getenv("SARA_USE_GPU", "0") == "1"

        config = {
            True: {
                "model": "medium",
                "device": "cuda",
                "compute_type": "float16",
            },
            False: {
                "model": "small",
                "device": "cpu",
                "compute_type": "int8",
            },
        }[usar_gpu]

        self.fs = 16000
        self.modelo = WhisperModel(
            config["model"],
            device=config["device"],
            compute_type=config["compute_type"],
        )
        self.vad = webrtcvad.Vad(3)
        self.fila_eventos = fila
        self.audio_bus = audio_bus

    def _tocar_som(self, arquivo):
        subprocess.run([
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel",
            "quiet",
            str(arquivo)
        ])

    def _capturar_fala(self):
        fila_audio = self.audio_bus.subscribe()

        try:
            self._tocar_som(SOUNDS / "start-stream.mp3")
            self.audio_bus.flush(fila_audio)

            print("[STT] Gravando...")

            self.fila_eventos.put(FalaUsuarioIniciada())

            frames = []

            MAX_INITIAL_SILENCE = MAX_INITIAL_SILENCE_MS // FRAME_MS
            MAX_END_SILENCE = MAX_END_SILENCE_MS // FRAME_MS
            MIN_SPEECH_FRAMES = MIN_SPEECH_MS // FRAME_MS

            initial_silence_frames = 0
            silence_frames = 0
            speech_frames = 0
            fala_iniciada = False

            while True:
                chunk = fila_audio.get()

                is_speech = (
                    chunk.rms > RMS_MINIMO_FALA and
                    self.vad.is_speech(chunk.samples.tobytes(), self.fs)
                )

                if is_speech:
                    speech_frames += 1
                    silence_frames = 0
                    frames.append(chunk.samples.copy())

                    if speech_frames >= MIN_SPEECH_FRAMES:
                        fala_iniciada = True

                else:
                    if fala_iniciada:
                        silence_frames += 1

                        if silence_frames > MAX_END_SILENCE:
                            break

                    else:
                        if speech_frames > 0:
                            frames.clear()

                        speech_frames = 0
                        initial_silence_frames += 1

                        if initial_silence_frames > MAX_INITIAL_SILENCE:
                            break

            self._tocar_som(SOUNDS / "end-stream.mp3")

            print("[STT] Fim da gravação.")
            self.fila_eventos.put(FalaUsuarioFinalizada())

            if frames:
                recording = np.concatenate(frames)
            else:
                recording = np.empty(0, dtype=np.int16)

            return recording.astype(np.float32) / 32768.0

        finally:
            self.audio_bus.unsubscribe(fila_audio)


    def _transcrever_audio(self, audio):
        if audio.size == 0:
            return ""

        segments, info = self.modelo.transcribe(
            audio,
            language="pt",
            vad_filter=True
        )

        return " ".join(segment.text.strip() for segment in segments).strip()


    def _ouvir_e_transcrever(self):
        audio = self._capturar_fala()
        texto = self._transcrever_audio(audio)

        self.fila_eventos.put(FalaUsuarioTranscrita(texto))


    def ouvir_e_transcrever_async(self):
        self.thread_ouvir_e_transcrever = threading.Thread(
            target=self._ouvir_e_transcrever,
            daemon=True
        )
        self.thread_ouvir_e_transcrever.start()

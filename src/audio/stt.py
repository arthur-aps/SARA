import subprocess
import os

import numpy as np
import soundfile as sf
import webrtcvad
import threading

from config.paths import SOUNDS
from config.paths import RECORDINGS

from faster_whisper import WhisperModel

from eventos import (
    FalaUsuarioIniciada,
    FalaUsuarioFinalizada,
    FalaUsuarioArquivada,
    FalaUsuarioTranscrita
)

from audio import AudioChunk


class STT:

    def __init__(self, fila, audio_bus, request_path=(RECORDINGS / "request.wav")):
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
        self.REQUEST_PATH = request_path

    def _gravar(self):
        path = self.REQUEST_PATH

        fila_audio = self.audio_bus.subscribe()

        try:
            subprocess.run([
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "quiet",
                str(SOUNDS / "start-stream.mp3")
            ])

            self.audio_bus.flush(fila_audio)

            print("[STT] Gravando...")

            self.fila_eventos.put(FalaUsuarioIniciada())

            frames = []

            FRAME_MS = 20

            MAX_INITIAL_SILENCE_MS = 300
            MAX_END_SILENCE_MS = 700
            MIN_SPEECH_MS = 100

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
                    chunk.rms > 650 and
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

            subprocess.run([
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "quiet",
                str(SOUNDS / "end-stream.mp3")
            ])

            print("[STT] Fim da gravação.")
            self.fila_eventos.put(FalaUsuarioFinalizada(path))

            recording = np.frombuffer(
                b"".join(frames),
                dtype=np.int16
            )

            recording = recording.astype(np.float32) / 32768.0

            sf.write(path, recording, self.fs)
            self.fila_eventos.put(FalaUsuarioArquivada(path))

        finally:
            self.audio_bus.unsubscribe(fila_audio)


    def gravar_async(self):
        self.thread_gravar = threading.Thread(
            target=self._gravar,
            daemon=True
        ).start()


    def _transcrever(self):
        audio = self.REQUEST_PATH

        segments, info = self.modelo.transcribe(
            audio,
            language="pt",
            vad_filter=True
        )

        texto = " ".join(segment.text for segment in segments)

        self.fila_eventos.put(FalaUsuarioTranscrita(texto))

    def transcrever_async(self):
        self.thread_transcrever = threading.Thread(
            target=self._transcrever,
            daemon=True
        )
        self.thread_transcrever.start()
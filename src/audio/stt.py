import subprocess

import numpy as np
import pyaudio
import soundfile as sf
import webrtcvad
import threading

from config.paths import SOUNDS
from config.paths import RECORDINGS

from faster_whisper import WhisperModel

from eventos import Evento


class STT:

    def __init__(self, fila, audio_bus, request_path=(RECORDINGS / "request.wav")):
        self.fs = 16000
        self.modelo = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )
        self.vad = webrtcvad.Vad(2)
        self.audio = pyaudio.PyAudio()
        self.fila_eventos = fila
        self.fila_audio = audio_bus.subscribe()
        self.REQUEST_PATH = request_path

    def _gravar(self):
        path = self.REQUEST_PATH
        frames = []

        silencio = 0
        falando = False

        subprocess.run([
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel",
            "quiet",
            str(SOUNDS / "start-stream.mp3")
        ])

        print("[STT] Gravando...")
        self.fila_eventos.put(Evento.FALA_USUARIO_INICIADA)

        while True:

            chunk = self.fila_audio.get()

            is_speech = self.vad.is_speech(chunk, self.fs)

            if is_speech:
                falando = True
                silencio = 0
                frames.append(chunk)

            elif falando:

                silencio += 1
                frames.append(chunk)

                if silencio > 150:
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
        self.fila_eventos.put(Evento.FALA_USUARIO_FINALIZADA)

        recording = np.frombuffer(
            b"".join(frames),
            dtype=np.int16
        )

        recording = recording.astype(np.float32) / 32768.0

        sf.write(path, recording, self.fs)

        self.fila_eventos.put(Evento.FALA_USUARIO_ARQUIVADA)
        return path

    def gravar_async(self):
        self.thread_gravar = threading.Thread(
            target=self._gravar,
            daemon=True
        )
        self.thread_gravar.start()

    def _transcrever(self):
        audio = self.REQUEST_PATH

        segments, info = self.modelo.transcribe(
            audio,
            language="pt",
            vad_filter=True
        )

        self.fila_eventos.put(Evento.FALA_USUARIO_TRANSCRITA)
        return " ".join(segment.text for segment in segments)

    def transcrever_async(self):
        self.thread_transcrever = threading.Thread(
            target=self._transcrever,
            daemon=True
        )
        self.thread_transcrever.start()
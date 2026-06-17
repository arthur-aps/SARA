import edge_tts
import asyncio
import subprocess

from faster_whisper import WhisperModel
import sounddevice as sd
import soundfile as sf
import pyaudio
import numpy as np
import webrtcvad
import collections

REQUEST_PATH = "recordings/request.wav"
RESPONSE_PATH = "recordings/response.mp3"

modeloWhisper = WhisperModel("small", device="cpu", compute_type="int8")
duration = 5  # seconds
fs = 16000  # sample rate
sd.default.samplerate = fs
sd.default.channels = 1
sd.default.dtype = 'float32'

# Text to Speech da SARA, usando a voz "pt-BR-FranciscaNeural" do Microsoft Edge
async def falar_async(texto, audio_file=RESPONSE_PATH):
    communicate = edge_tts.Communicate(texto, voice="pt-BR-FranciscaNeural")
    await communicate.save(audio_file)
    subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", audio_file])

def falar(texto):
    asyncio.run(falar_async(texto))

# Gravação e transcrição de áudio
def gravar(audio_file=REQUEST_PATH):
    subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", "sounds/start-stream.mp3"])
    print("gravando...")
    vad = webrtcvad.Vad(2)  # agressividade 0-3
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=320
    )
    
    frames = []
    silencio = 0
    falando = False
    
    # continua escutando até o usuário ficar quieto
    while True:
        chunk = stream.read(320)  # 20ms de áudio
        is_speech = vad.is_speech(chunk, 16000)
        
        if is_speech:
            falando = True
            silencio = 0
            frames.append(chunk)
        elif falando:
            silencio += 1
            frames.append(chunk)
            if silencio > 50:
                break
    
    subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", "sounds/end-stream.mp3"])
    print("fim da gravação.")
    recording = np.frombuffer(b''.join(frames), dtype=np.int16)
    recording = recording.astype(np.float32) / 32768.0

    sf.write(audio_file, recording, fs)
    return audio_file

def transcrever(audio):
    segments, info = modeloWhisper.transcribe(audio, language="pt", vad_filter=True)
    texto = " ".join([segment.text for segment in segments])
    return texto
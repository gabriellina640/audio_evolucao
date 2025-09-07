import sounddevice as sd
from scipy.io.wavfile import write

def gravar_audio(arquivo="audio.wav", duracao=10, fs=44100):
    """
    Grava áudio do microfone e salva em arquivo WAV
    """
    print("Gravando...")
    audio = sd.rec(int(duracao * fs), samplerate=fs, channels=1)
    sd.wait()
    write(arquivo, fs, audio)
    print(f"Áudio salvo em {arquivo}")
    return arquivo
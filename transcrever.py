import openai
import os

# Carrega chave da variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcrever_audio(arquivo_audio):
    """
    Transcreve um arquivo de áudio usando Whisper
    """
    with open(arquivo_audio, "rb") as f:
        resultado = openai.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return resultado.text
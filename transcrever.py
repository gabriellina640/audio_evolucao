import openai
import os
from dotenv import load_dotenv

# Carrega a variável OPENAI_API_KEY do .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY não encontrada. Verifique seu arquivo .env ou variável de ambiente.")

openai.api_key = api_key

def transcrever_audio(arquivo_audio):
    """
    Transcreve um arquivo de áudio usando Whisper (OpenAI)
    """
    try:
        with open(arquivo_audio, "rb") as f:
            resultado = openai.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return resultado.text
    except Exception as e:
        return f"❌ Erro ao transcrever áudio: {str(e)}"

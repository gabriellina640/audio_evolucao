from openai import OpenAI

def transcrever_audio(client: OpenAI, arquivo_audio: str) -> str:
    """
    Transcreve um ficheiro de áudio usando o modelo Whisper da OpenAI.

    Args:
        client: O cliente da API OpenAI já inicializado.
        arquivo_audio: O caminho para o ficheiro de áudio a ser transcrito.

    Returns:
        O texto transcrito.
    """
    try:
        with open(arquivo_audio, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
              model="whisper-1",
              file=audio_file
            )
        return transcription.text
    except Exception as e:
        print(f"ERRO na transcrição: {e}")
        # Lança a exceção para que a função principal a possa tratar
        raise e

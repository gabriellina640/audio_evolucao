import gradio as gr
import tempfile
import soundfile as sf
from transcrever import transcrever_audio
from preencher import preencher_evolucao
from pydub import AudioSegment
import os
from dotenv import load_dotenv
import openai
from pydub.utils import which  # para localizar ffmpeg/ffprobe no sistema

# ----------------------------
# Carrega a variável OPENAI_API_KEY do .env
# ----------------------------
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------------------------
# Configuração do FFmpeg no Ubuntu (usa o instalado no sistema)
# ----------------------------
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

print("Usando FFmpeg em:", AudioSegment.converter)
print("Usando FFprobe em:", AudioSegment.ffprobe)

# ----------------------------
# Função principal de processamento de áudio
# ----------------------------
def processar_audio(arquivo_audio):
    """
    Recebe áudio (numpy), salva em arquivo temporário, transcreve e preenche a evolução
    """
    if arquivo_audio is None:
        return "⚠️ Nenhum áudio foi recebido. Grave ou envie novamente."

    sr, data = arquivo_audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        sf.write(temp_wav.name, data, sr)
        temp_path = temp_wav.name

    print("DEBUG - arquivo temporário salvo em:", temp_path)

    try:
        texto = transcrever_audio(temp_path)
        evolucao = preencher_evolucao(texto)
        return evolucao
    except Exception as e:
        return f"❌ Erro ao processar áudio: {str(e)}"
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# ----------------------------
# Interface Gradio
# ----------------------------
interface = gr.Interface(
    fn=processar_audio,
    inputs=gr.Audio(sources=["upload", "microphone"], type="numpy", label="Envie ou grave um áudio"),
    outputs=gr.Textbox(label="Evolução Preenchida", lines=25),
    title="Transcrição e Evolução Médica",
    description="Envie ou grave um áudio. O sistema transcreve e preenche automaticamente a evolução padrão."
)

# ----------------------------
# Launch
# ----------------------------
if __name__ == "__main__":
    interface.launch(share=False)

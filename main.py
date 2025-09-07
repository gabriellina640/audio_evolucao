import gradio as gr
import tempfile
import soundfile as sf
from transcrever import transcrever_audio
from preencher import preencher_evolucao
from pydub import AudioSegment
import os

# ----------------------------
# Configuração do FFmpeg dentro do projeto
# ----------------------------
base_path = os.path.join(os.path.dirname(__file__), "ffmpeg", "bin")

# Adiciona temporariamente ao PATH do Python
os.environ["PATH"] = base_path + os.pathsep + os.environ.get("PATH", "")

# Define explicitamente os executáveis para o pydub
AudioSegment.converter = os.path.join(base_path, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(base_path, "ffprobe.exe")

# DEBUG: verifica se os caminhos estão corretos
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

    # Gradio retorna (sample_rate, data)
    sr, data = arquivo_audio
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(temp_wav.name, data, sr)  # salva o áudio em .wav

    print("DEBUG - arquivo temporário salvo em:", temp_wav.name)

    try:
        texto = transcrever_audio(temp_wav.name)
        evolucao = preencher_evolucao(texto)
        return evolucao
    except Exception as e:
        return f"❌ Erro ao processar áudio: {str(e)}"

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
    # share=True se quiser link público
    interface.launch(share=False)

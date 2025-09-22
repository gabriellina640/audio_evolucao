import gradio as gr
import tempfile
import soundfile as sf
import os
import platform
from openai import OpenAI
from pydub import AudioSegment
from pydub.utils import which

# Funções importadas dos nossos módulos
from transcrever import transcrever_audio
from preencher import preencher_evolucao

# ----------------------------
# Configuração do FFmpeg para portabilidade (Windows/Linux)
# ----------------------------
if platform.system() == "Windows":
    print("Sistema Windows detectado. Usando FFmpeg local.")
    AudioSegment.converter = os.path.join("ffmpeg", "bin", "ffmpeg.exe")
    AudioSegment.ffprobe = os.path.join("ffmpeg", "bin", "ffprobe.exe")
else:
    converter_path = which("ffmpeg")
    if not converter_path:
        print("AVISO CRÍTICO: FFmpeg não foi encontrado no sistema.")
        print("Se estiver no Hugging Face, certifique-se de que o ficheiro 'packages.txt' existe e contém 'ffmpeg'.")

# ----------------------------
# Inicialização Centralizada do Cliente OpenAI
# ----------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Ficheiro .env carregado para desenvolvimento local.")
except ImportError:
    print("dotenv não instalado. No servidor, as chaves virão dos Secrets.")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------
# Função principal que orquestra o fluxo de trabalho
# ----------------------------
def processar_audio(arquivo_audio):
    if arquivo_audio is None:
        return "⚠️ Nenhum áudio foi recebido. Grave ou envie novamente."
    
    sr, data = arquivo_audio
    temp_path = None
    try:
        # Salva o áudio recebido num ficheiro temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            sf.write(temp_wav.name, data, sr)
            temp_path = temp_wav.name
        
        # Etapa 1: Transcrever o áudio
        print("Iniciando transcrição...")
        texto_transcrito = transcrever_audio(client, temp_path)
        print("Transcrição concluída.")
        
        # Etapa 2: Preencher a evolução com o texto
        print("Iniciando preenchimento da evolução...")
        evolucao_preenchida = preencher_evolucao(client, texto_transcrito)
        print("Evolução preenchida.")
        
        return evolucao_preenchida
        
    except Exception as e:
        print(f"ERRO no fluxo principal (app.py): {e}")
        return f"❌ Ocorreu um erro ao processar o áudio. Verifique se a sua chave de API da OpenAI está configurada corretamente nos Secrets do Hugging Face e tente novamente."
        
    finally:
        # Garante que o ficheiro temporário seja sempre deletado
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

# ----------------------------
# Interface Gráfica e Lançamento
# ----------------------------
interface = gr.Interface(
    fn=processar_audio,
    inputs=gr.Audio(sources=["upload", "microphone"], type="numpy", label="Envie ou grave um áudio"),
    outputs=gr.Textbox(label="Evolução Preenchida", lines=25, show_copy_button=True),
    title="Assistente de Evolução Médica",
    description="Envie ou grave um áudio com o relato do paciente. O sistema irá transcrever o áudio e preencher automaticamente um modelo de evolução médica padrão."
)

if __name__ == "__main__":
    interface.launch()
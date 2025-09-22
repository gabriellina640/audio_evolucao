import gradio as gr
import tempfile
import soundfile as sf
from transcrever import transcrever_audio
from preencher import preencher_evolucao
import os
import openai

# Imports para configuração inteligente do FFmpeg
from pydub import AudioSegment
from pydub.utils import which
import platform

# ----------------------------
# Configuração do FFmpeg para portabilidade (Windows/Linux)
# ----------------------------
# Esta lógica garante que o app encontre o FFmpeg em diferentes sistemas.
print("Verificando sistema operacional para configurar o FFmpeg...")
if platform.system() == "Windows":
    # Em um ambiente Windows, apontamos para a pasta ffmpeg local do projeto.
    # Isso é ideal para desenvolvimento local sem precisar instalar nada globalmente.
    print("Sistema Windows detectado. Usando FFmpeg local.")
    AudioSegment.converter = os.path.join("ffmpeg", "bin", "ffmpeg.exe")
    AudioSegment.ffprobe = os.path.join("ffmpeg", "bin", "ffprobe.exe")
else:
    # Em ambientes Linux (como Hugging Face/Ubuntu), o pydub encontrará o FFmpeg
    # automaticamente se ele estiver instalado no sistema. A linha abaixo é uma
    # verificação extra para garantir que ele foi encontrado.
    converter_path = which("ffmpeg")
    if converter_path:
        print(f"Sistema Linux/Outro detectado. FFmpeg encontrado em: {converter_path}")
    else:
        print("--------------------------------------------------------------------")
        print("AVISO CRÍTICO: FFmpeg não foi encontrado no sistema.")
        print("O processamento de áudio provavelmente irá falhar.")
        print("Se estiver no Hugging Face, crie um arquivo 'packages.txt' e adicione a linha 'ffmpeg' nele.")
        print("--------------------------------------------------------------------")

# ----------------------------
# Carrega a variável OPENAI_API_KEY
# No Hugging Face, isso virá dos "Secrets" do Space.
# Localmente, você pode usar um arquivo .env com a biblioteca python-dotenv.
# ----------------------------
# A importação do dotenv é opcional no servidor, mas não causa erro.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("dotenv não instalado, pulando. Essencial para rodar localmente com .env")

openai.api_key = os.getenv("OPENAI_API_KEY")

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
    
    # Usamos um arquivo temporário para salvar o áudio
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            sf.write(temp_wav.name, data, sr)
            temp_path = temp_wav.name
        
        print("DEBUG - arquivo temporário salvo em:", temp_path)
        
        texto = transcrever_audio(temp_path)
        evolucao = preencher_evolucao(texto)
        return evolucao
        
    except Exception as e:
        # Retorna uma mensagem de erro clara para o usuário
        print(f"ERRO: {e}") # Log do erro no console
        return f"❌ Erro ao processar áudio. Verifique os logs do servidor ou sua chave de API."
        
    finally:
        # Garante que o arquivo temporário seja sempre deletado
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            print("DEBUG - arquivo temporário removido:", temp_path)

# ----------------------------
# Interface Gradio
# ----------------------------
interface = gr.Interface(
    fn=processar_audio,
    inputs=gr.Audio(sources=["upload", "microphone"], type="numpy", label="Envie ou grave um áudio"),
    outputs=gr.Textbox(label="Evolução Preenchida", lines=25, placeholder="O texto da evolução médica aparecerá aqui..."),
    title="Transcrição e Evolução Médica",
    description="Envie ou grave um áudio. O sistema transcreve usando a API da OpenAI e preenche automaticamente um modelo de evolução médica."
)

# ----------------------------
# Launch
# ----------------------------
if __name__ == "__main__":
    interface.launch()


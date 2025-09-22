import gradio as gr
import tempfile
import soundfile as sf
<<<<<<< HEAD
import os
import platform
from openai import OpenAI
from pydub import AudioSegment
from pydub.utils import which

# Funções importadas dos nossos módulos
from transcrever import transcrever_audio
from preencher import preencher_evolucao
=======
from transcrever import transcrever_audio
from preencher import preencher_evolucao
import os
import openai

# Imports para configuração inteligente do FFmpeg
from pydub import AudioSegment
from pydub.utils import which
import platform
>>>>>>> 957320191d7e226b38f3c9ab54d2edd6bb47d8f4

# ----------------------------
# Configuração do FFmpeg para portabilidade (Windows/Linux)
# ----------------------------
<<<<<<< HEAD
if platform.system() == "Windows":
=======
# Esta lógica garante que o app encontre o FFmpeg em diferentes sistemas.
print("Verificando sistema operacional para configurar o FFmpeg...")
if platform.system() == "Windows":
    # Em um ambiente Windows, apontamos para a pasta ffmpeg local do projeto.
    # Isso é ideal para desenvolvimento local sem precisar instalar nada globalmente.
>>>>>>> 957320191d7e226b38f3c9ab54d2edd6bb47d8f4
    print("Sistema Windows detectado. Usando FFmpeg local.")
    AudioSegment.converter = os.path.join("ffmpeg", "bin", "ffmpeg.exe")
    AudioSegment.ffprobe = os.path.join("ffmpeg", "bin", "ffprobe.exe")
else:
<<<<<<< HEAD
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
=======
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
>>>>>>> 957320191d7e226b38f3c9ab54d2edd6bb47d8f4
    if arquivo_audio is None:
        return "⚠️ Nenhum áudio foi recebido. Grave ou envie novamente."
    
    sr, data = arquivo_audio
<<<<<<< HEAD
    temp_path = None
    try:
        # Salva o áudio recebido num ficheiro temporário
=======
    
    # Usamos um arquivo temporário para salvar o áudio
    temp_path = None
    try:
>>>>>>> 957320191d7e226b38f3c9ab54d2edd6bb47d8f4
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            sf.write(temp_wav.name, data, sr)
            temp_path = temp_wav.name
        
<<<<<<< HEAD
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
=======
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
>>>>>>> 957320191d7e226b38f3c9ab54d2edd6bb47d8f4
# ----------------------------
interface = gr.Interface(
    fn=processar_audio,
    inputs=gr.Audio(sources=["upload", "microphone"], type="numpy", label="Envie ou grave um áudio"),
<<<<<<< HEAD
    outputs=gr.Textbox(label="Evolução Preenchida", lines=25, show_copy_button=True),
    title="Assistente de Evolução Médica",
    description="Envie ou grave um áudio com o relato do paciente. O sistema irá transcrever o áudio e preencher automaticamente um modelo de evolução médica padrão."
)

if __name__ == "__main__":
    interface.launch()
=======
    outputs=gr.Textbox(label="Evolução Preenchida", lines=25, placeholder="O texto da evolução médica aparecerá aqui..."),
    title="Transcrição e Evolução Médica",
    description="Envie ou grave um áudio. O sistema transcreve usando a API da OpenAI e preenche automaticamente um modelo de evolução médica."
)

# ----------------------------
# Launch
# ----------------------------
if __name__ == "__main__":
    interface.launch()

>>>>>>> 957320191d7e226b38f3c9ab54d2edd6bb47d8f4

import gradio as gr
import os
import platform
from openai import OpenAI
from pydub import AudioSegment
from pydub.utils import which
import traceback
import httpx
import base64
import tempfile

# ***** NOVO: Importações para a nossa API dedicada *****
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

# Funções importadas dos seus módulos
from transcrever import transcrever_audio
from preencher import preencher_evolucao

# ----------------------------
# Configuração do FFmpeg e OpenAI (sem alterações)
# ----------------------------
if platform.system() == "Windows":
    AudioSegment.converter = os.path.abspath(os.path.join("ffmpeg", "bin", "ffmpeg.exe"))
    AudioSegment.ffprobe = os.path.abspath(os.path.join("ffmpeg", "bin", "ffprobe.exe"))
else:
    if not which("ffmpeg"): print("AVISO CRÍTICO: FFmpeg não encontrado.")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("ERRO CRÍTICO: OPENAI_API_KEY não encontrada!")

custom_httpx_client = httpx.Client(verify=False)
client = OpenAI(api_key=api_key, http_client=custom_httpx_client)
print("Cliente OpenAI inicializado.")

# ----------------------------
# Função principal (sem alterações)
# ----------------------------
def processar_audio_api_fn(arquivo_audio_path):
    try:
        print(f"\n--- A iniciar processamento para: {arquivo_audio_path} ---")
        texto_transcrito = transcrever_audio(client, arquivo_audio_path)
        evolucao_preenchida = preencher_evolucao(client, texto_transcrito)
        print("--- Processamento concluído com sucesso! ---")
        return evolucao_preenchida
    except Exception as e:
        print("\n!!!!!!!!!!!!!! OCORREU UM ERRO !!!!!!!!!!!!!!")
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        return f"❌ Ocorreu um erro interno no servidor. Verifique o terminal do serviço de IA para detalhes."

# ----------------------------
# Interface Gráfica do Gradio (Porta 1 para humanos)
# ----------------------------
interface_gradio = gr.Interface(
    fn=processar_audio_api_fn,
    inputs=gr.Audio(type="filepath", label="Ficheiro de Áudio"),
    outputs=gr.Textbox(label="Evolução Preenchida", lines=25),
    title="Assistente de Evolução Médica (UI de Teste)",
    description="Interface para testar o serviço de transcrição diretamente."
)

# ----------------------------
# ***** NOVO: A nossa API dedicada com FastAPI (Porta 2 para o Laravel) *****
# ----------------------------
api_fastapi = FastAPI()

# Modelo para validar o pedido que vem do Laravel
class AudioRequest(BaseModel):
    audio_base64: str
    file_extension: str # Ex: 'mp3', 'wav'

@api_fastapi.post("/transcrever")
def transcrever_endpoint(request: AudioRequest):
    try:
        # 1. Descodificar o áudio Base64
        audio_data = base64.b64decode(request.audio_base64)
        
        # 2. Salvar num ficheiro temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{request.file_extension}") as temp_audio_file:
            temp_audio_file.write(audio_data)
            temp_filepath = temp_audio_file.name
        
        # 3. Chamar a nossa função principal com o caminho do ficheiro
        resultado = processar_audio_api_fn(temp_filepath)
        
        # 4. Limpar o ficheiro temporário
        os.unlink(temp_filepath)
        
        if "❌" in resultado: # Se a função principal retornou um erro
             return {"status": "error", "message": resultado}
        
        return {"status": "success", "transcription": resultado}

    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": f"Erro crítico na API: {e}"}

# ----------------------------
# Monta a API FastAPI e a Interface Gradio juntas
# ----------------------------
app = gr.mount_gradio_app(api_fastapi, interface_gradio, path="/")

if __name__ == "__main__":
    print("\nA iniciar o servidor Gradio com API dedicada na porta 7860...")
    uvicorn.run(app, host="0.0.0.0", port=7860)


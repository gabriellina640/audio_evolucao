import openai
import os
from dotenv import load_dotenv

# ----------------------------
# Carrega chave da variável de ambiente
# ----------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY não encontrada. Verifique seu arquivo .env ou variável de ambiente.")

openai.api_key = api_key

# ----------------------------
# Modelo de evolução padrão
# ----------------------------
MODELO_ESTRUTURA = """
Preencha o seguinte modelo de evolução padrão com as informações do áudio transcrito:

🔹 Estrutura da Evolução Padrão

Identificação do Paciente:
Nome:
Idade:
Leito/Enfermaria:

Data/Hora da Evolução: [dd/mm/aaaa - hh:mm]

Queixa Principal (QP):

História da Doença Atual (HDA):

Antecedentes Pessoais/Patológicos (APP):

Medicações em Uso:

Alergias:

Exame Físico (EF):
Estado geral:
Sinais vitais:
Cabeça e pescoço:
Tórax:
Abdome:
Extremidades:
Neurológico:

Exames Complementares (se citados):

Conduta / Plano:
"""

# ----------------------------
# Função para preencher evolução
# ----------------------------
def preencher_evolucao(texto_transcrito):
    """
    Recebe o texto transcrito e retorna a evolução preenchida usando o modelo GPT.
    """
    try:
        prompt = f"Transcrevi o seguinte áudio:\n\n{texto_transcrito}\n\nPreencha o modelo de evolução padrão:\n{MODELO_ESTRUTURA}"
        
        resposta = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return resposta.choices[0].message.content
    except Exception as e:
        return f"❌ Erro ao preencher evolução: {str(e)}"

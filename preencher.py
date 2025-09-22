from openai import OpenAI

# ----------------------------
# Modelo de evolução padrão
# ----------------------------
MODELO_ESTRUTURA = """
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
def preencher_evolucao(client: OpenAI, texto_transcrito: str) -> str:
    """
    Recebe o texto transcrito e retorna a evolução preenchida usando o modelo GPT.

    Args:
        client: O cliente da API OpenAI já inicializado.
        texto_transcrito: O texto do áudio já transcrito.

    Returns:
        O modelo de evolução preenchido.
    """
    try:
        prompt = f"Com base no seguinte áudio transcrito de um profissional de saúde, preencha o modelo de evolução médica de forma clara e objetiva.\n\nÁudio Transcrito:\n--- \n{texto_transcrito}\n---\n\n{MODELO_ESTRUTURA}"

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return resposta.choices[0].message.content
    except Exception as e:
        print(f"ERRO ao preencher evolução: {e}")
        # Lança a exceção para que a função principal a possa tratar
        raise e

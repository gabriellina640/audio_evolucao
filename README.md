Transcrição e Evolução Médica com IA
Este projeto utiliza a API da OpenAI para transcrever áudios e preencher automaticamente um modelo de evolução médica.

Funcionalidades
Transcrição de áudio via upload de arquivo ou gravação pelo microfone.

Preenchimento automático de um prontuário de evolução médica com base no texto transcrito.

Interface web interativa criada com Gradio.

🚀 Como Executar o Projeto
Este aplicativo foi projetado para ser portátil, funcionando tanto em um ambiente de desenvolvimento local (Windows) quanto em uma plataforma de hospedagem (Linux, como o Hugging Face Spaces).

1. Configuração em um Ambiente Local (Windows)
Siga estes passos para rodar o aplicativo no seu computador.

a. Clone o Repositório:

git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA>

b. Instale o FFmpeg (Dependência de Áudio):
Este projeto precisa do FFmpeg para processar áudios.

Baixe a versão mais recente do FFmpeg em: https://ffmpeg.org/download.html

Descompacte o arquivo.

Dentro da pasta do seu projeto, crie a seguinte estrutura de pastas: ffmpeg/bin/.

Copie os arquivos ffmpeg.exe e ffprobe.exe da pasta que você baixou para dentro de ffmpeg/bin/.

c. Crie o Arquivo de Chave de API:

Na raiz do projeto, crie um arquivo chamado .env.

Dentro deste arquivo, adicione sua chave da OpenAI:

OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxx"

d. Instale as Bibliotecas Python:

pip install -r requirements.txt

e. Execute o Aplicativo:

python app.py

Agora, você pode acessar a interface no endereço local que aparecer no seu terminal.

2. Deploy no Hugging Face Spaces
Para hospedar seu aplicativo online e de graça.

a. Crie um packages.txt:
Na raiz do seu projeto, crie um arquivo packages.txt com o seguinte conteúdo:

ffmpeg

b. Configure os "Secrets":

No seu Space do Hugging Face, vá para a aba "Settings".

Na seção "Secrets", clique em "New secret".

Crie um secret com o nome OPENAI_API_KEY e cole sua chave da OpenAI como valor.

c. Envie seus Arquivos:
Envie todos os seus arquivos (app.py, requirements.txt, packages.txt, etc.) para o repositório do seu Space. A plataforma cuidará do resto automaticamente.
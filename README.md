# Meu Assistente LLM

Aplicação de terminal em Python que envia uma mensagem ao Google Gemini e imprime a resposta.

## Requisitos

- Python 3.10 ou superior
- Uma chave de API do Google AI Studio

## Configuração no Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite `.env` e substitua `sua_chave_aqui` pela sua chave. Esse arquivo é ignorado pelo Git; não compartilhe nem versione a chave.

## Executar

```powershell
python src/main.py
```

O modelo padrão é `gemini-2.5-flash`. É possível alterá-lo em `GEMINI_MODEL` no `.env`. A chave também pode ser definida diretamente no ambiente como `GEMINI_API_KEY`.

## Publicar a etapa básica

Depois de configurar sua URL real do GitHub, execute:

```powershell
git init
git add .
git commit -m "feat: implementa fluxo básico de consulta ao LLM via terminal"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/meu-assistente-llm.git
git push -u origin main
git tag -a p0-basico -m "Entrega do Nível Básico (p0-basico)"
git push origin p0-basico
```

Troque `SEU_USUARIO` pela conta ou organização correta. O arquivo `.env.example` contém apenas valores de referência; o `.env` com sua chave não deve ser enviado ao repositório.

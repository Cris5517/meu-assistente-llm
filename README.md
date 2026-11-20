# Meu Assistente LLM

Aplicativo de terminal em Python para enviar perguntas ao Google Gemini e imprimir respostas textuais.

## Requisitos documentados

- Sistema operacional: Windows 10/11 ou Linux/macOS
- Python: 3.12.10 (versão usada no desenvolvimento)
- `google-genai`: 3.6.1
- `python-dotenv`: 1.2.4

Outras versões de Python 3.10 ou superiores podem funcionar, mas a reprodução oficial usa Python 3.12.10.

## Instalação limpa no Windows PowerShell

Em uma pasta vazia:

```powershell
git clone https://github.com/Cris5517/meu-assistente-llm.git
cd meu-assistente-llm
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Se o PowerShell bloquear a ativação, execute somente nesta sessão:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

No Linux/macOS:

```bash
git clone https://github.com/Cris5517/meu-assistente-llm.git
cd meu-assistente-llm
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

## Configuração

Edite `.env` e substitua `sua_chave_aqui` pela chave obtida no Google AI Studio. A chave também pode ser fornecida como variável de ambiente.

| Variável | Padrão | Uso |
|---|---|---|
| `GEMINI_API_KEY` | nenhuma | Autenticação; obrigatória |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Modelo usado |
| `GEMINI_TEMPERATURE` | `0.7` | Criatividade; intervalo `0` a `1` |
| `GEMINI_TOP_P` | `0.95` | Amostragem cumulativa; intervalo `0` a `1` |
| `GEMINI_TOP_K` | `40` | Quantidade de candidatos; inteiro maior que zero |
| `GEMINI_MAX_OUTPUT_TOKENS` | `1024` | Limite de saída; inteiro maior que zero |

As configurações são alteradas no `.env` ou no ambiente do sistema; não exigem mudança no código.

## Segurança e registros

- `.env` é ignorado pelo Git e não deve ser enviado ao repositório.
- A chave nunca é armazenada no código ou nos registros.
- Os registros informam eventos e tipos de falha, sem gravar prompts, respostas, tokens, credenciais ou dados pessoais.
- Em caso de saída sensível inesperada, revise o código antes de ativar outro nível de log.

## Executar

```powershell
python src/main.py
```

Digite uma mensagem no terminal. Uma entrada vazia é rejeitada antes da chamada ao modelo.

## Testes locais sem rede

Execute:

```powershell
python -m unittest discover -s tests -v
```

Os testes cobrem entrada vazia, normalização da entrada, carregamento e validação de configuração, resposta simulada e propagação de erro simulado. Nenhum teste realiza chamada real ao Gemini.

## Validação em ambiente limpo

1. Crie um novo ambiente virtual seguindo a seção de instalação.
2. Confirme que a instalação foi concluída sem erros:

```powershell
python -m pip check
python -m unittest discover -s tests -v
```

3. Execute `python src/main.py` com `.env` configurado e faça uma única pergunta curta.
4. Confirme que `.env` não aparece em `git status`.
5. Use outra pergunta para confirmar que a alteração de `GEMINI_TEMPERATURE` ou outro parâmetro funciona sem editar o código.

Nenhuma chave foi usada ou registrada durante a preparação desta versão.

## Publicação e entrega avançada

Para publicar a versão final:

```powershell
git add .
git commit -m "feat: entrega avançada com configuração e testes locais"
git push origin main
git tag -a p0-avancado -m "Entrega do Nível Avançado (p0-avancado)"
git push origin p0-avancado
```

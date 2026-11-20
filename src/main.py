import os
import sys

from dotenv import load_dotenv
from google import genai


def obter_cliente() -> genai.Client:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Variável de ambiente GEMINI_API_KEY não encontrada. "
            "Configure-a no ambiente ou em um arquivo .env."
        )
    return genai.Client(api_key=api_key)


def gerar_resposta(cliente: genai.Client, prompt: str, modelo: str) -> str:
    resposta = cliente.models.generate_content(
        model=modelo,
        contents=prompt,
    )
    return resposta.text or "O modelo não retornou conteúdo textual."


def main() -> None:
    try:
        load_dotenv()
        modelo = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        pergunta = input("Digite sua mensagem: ").strip()

        if not pergunta:
            print("Entrada vazia. Informe um texto para enviar ao modelo.")
            sys.exit(1)

        cliente = obter_cliente()
        resposta = gerar_resposta(cliente, pergunta, modelo)
        print("\n--- Resposta do LLM ---")
        print(resposta)

    except RuntimeError as erro_config:
        print(f"Erro de configuração: {erro_config}", file=sys.stderr)
        sys.exit(1)
    except Exception as erro:
        print(f"Falha ao consultar o modelo: {erro}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

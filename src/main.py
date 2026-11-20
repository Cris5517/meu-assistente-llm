import logging
import os
import sys
from dataclasses import dataclass

from dotenv import load_dotenv
from google import genai
from google.genai import types


logger = logging.getLogger("meu-assistente-llm")


@dataclass(frozen=True)
class ConfiguracaoGeracao:
    modelo: str = "gemini-2.5-flash"
    temperatura: float = 0.7
    top_p: float = 0.95
    top_k: int = 40
    max_output_tokens: int = 1024


def validar_prompt(prompt: str) -> str:
    prompt_limpo = prompt.strip()
    if not prompt_limpo:
        raise ValueError("Entrada vazia. Informe um texto para enviar ao modelo.")
    return prompt_limpo


def _ler_float(nome: str, padrao: float) -> float:
    texto = os.getenv(nome)
    if texto is None:
        return padrao
    try:
        valor = float(texto)
    except ValueError:
        raise RuntimeError(f"Configuração inválida: {nome} deve ser numérico.")
    if not 0.0 <= valor <= 1.0:
        raise RuntimeError(f"Configuração inválida: {nome} deve estar entre 0 e 1.")
    return valor


def _ler_int(nome: str, padrao: int, minimo: int = 1) -> int:
    texto = os.getenv(nome)
    if texto is None:
        return padrao
    try:
        valor = int(texto)
    except ValueError:
        raise RuntimeError(f"Configuração inválida: {nome} deve ser inteiro.")
    if valor < minimo:
        raise RuntimeError(f"Configuração inválida: {nome} deve ser maior ou igual a {minimo}.")
    return valor


def carregar_configuracao() -> ConfiguracaoGeracao:
    load_dotenv()
    modelo = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    if not modelo:
        raise RuntimeError("Configuração inválida: GEMINI_MODEL não pode ficar vazio.")

    return ConfiguracaoGeracao(
        modelo=modelo,
        temperatura=_ler_float("GEMINI_TEMPERATURE", 0.7),
        top_p=_ler_float("GEMINI_TOP_P", 0.95),
        top_k=_ler_int("GEMINI_TOP_K", 40),
        max_output_tokens=_ler_int("GEMINI_MAX_OUTPUT_TOKENS", 1024),
    )


def obter_cliente() -> genai.Client:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Variável de ambiente GEMINI_API_KEY não encontrada. "
            "Configure-a no ambiente ou em um arquivo .env."
        )
    return genai.Client(api_key=api_key)


def gerar_resposta(cliente, prompt: str, configuracao: ConfiguracaoGeracao) -> str:
    resposta = cliente.models.generate_content(
        model=configuracao.modelo,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=configuracao.temperatura,
            top_p=configuracao.top_p,
            top_k=configuracao.top_k,
            max_output_tokens=configuracao.max_output_tokens,
        ),
    )
    return resposta.text or "O modelo não retornou conteúdo textual."


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    try:
        configuracao = carregar_configuracao()
        prompt = validar_prompt(input("Digite sua mensagem: "))
        cliente = obter_cliente()

        logger.info("Solicitação enviada ao modelo")
        resposta = gerar_resposta(cliente, prompt, configuracao)
        logger.info("Resposta recebida do modelo")

        print("\n--- Resposta do LLM ---")
        print(resposta)

    except (RuntimeError, ValueError) as erro:
        logger.warning("Falha esperada na execução")
        print(f"Erro: {erro}", file=sys.stderr)
        sys.exit(1)
    except Exception:
        logger.exception("Falha não esperada ao consultar o modelo")
        print("Falha ao consultar o modelo.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

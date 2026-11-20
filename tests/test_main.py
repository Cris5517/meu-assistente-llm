import os
import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.main import (
    ConfiguracaoGeracao,
    carregar_configuracao,
    gerar_resposta,
    validar_prompt,
)


class TesteLogicaLocal(unittest.TestCase):
    def tearDown(self):
        for nome in (
            "GEMINI_MODEL",
            "GEMINI_TEMPERATURE",
            "GEMINI_TOP_P",
            "GEMINI_TOP_K",
            "GEMINI_MAX_OUTPUT_TOKENS",
        ):
            os.environ.pop(nome, None)

    def test_entrada_vazia_eh_rejeitada(self):
        with self.assertRaises(ValueError):
            validar_prompt("   ")

    def test_entrada_eh_normalizada(self):
        self.assertEqual(validar_prompt("  Olá  "), "Olá")

    def test_configuracao_eh_carregada_sem_modificar_codigo(self):
        os.environ["GEMINI_MODEL"] = "modelo-teste"
        os.environ["GEMINI_TEMPERATURE"] = "0.25"
        os.environ["GEMINI_TOP_P"] = "0.8"
        os.environ["GEMINI_TOP_K"] = "20"
        os.environ["GEMINI_MAX_OUTPUT_TOKENS"] = "256"

        configuracao = carregar_configuracao()

        self.assertEqual(configuracao.modelo, "modelo-teste")
        self.assertEqual(configuracao.temperatura, 0.25)
        self.assertEqual(configuracao.top_p, 0.8)
        self.assertEqual(configuracao.top_k, 20)
        self.assertEqual(configuracao.max_output_tokens, 256)

    def test_configuracao_tem_limites_validos(self):
        os.environ["GEMINI_TEMPERATURE"] = "1.5"
        with self.assertRaisesRegex(RuntimeError, "GEMINI_TEMPERATURE"):
            carregar_configuracao()

    def test_resposta_simulada_eh_processada(self):
        class ModelosSimulados:
            def generate_content(self, **kwargs):
                self.kwargs = kwargs
                return SimpleNamespace(text="Resposta simulada")

        modelos = ModelosSimulados()
        cliente = SimpleNamespace(models=modelos)
        configuracao = ConfiguracaoGeracao(modelo="modelo-teste")

        resultado = gerar_resposta(cliente, "Pergunta", configuracao)

        self.assertEqual(resultado, "Resposta simulada")
        self.assertEqual(modelos.kwargs["model"], "modelo-teste")
        self.assertEqual(modelos.kwargs["contents"], "Pergunta")

    def test_erro_simulado_eh_propagado(self):
        class ClienteComErro:
            class Modelos:
                def generate_content(self, **kwargs):
                    raise RuntimeError("erro simulado")

            models = Modelos()

        with self.assertRaisesRegex(RuntimeError, "erro simulado"):
            gerar_resposta(ClienteComErro(), "Pergunta", ConfiguracaoGeracao())


if __name__ == "__main__":
    unittest.main()

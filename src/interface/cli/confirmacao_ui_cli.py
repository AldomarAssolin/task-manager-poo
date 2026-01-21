"""
Docstring para src.interface.cli.confirmacao_ui_cli

Implementação CLI da confirmação.
"""

from __future__ import annotations

from src.application.ports.confirmacao_ui import IConfirmacaoUI

class ConfirmacaoUICLI(IConfirmacaoUI):
    def confirmar(self, pergunta: str) -> bool:
        while True:
            resp = input(f"{pergunta} ").strip().lower()
            if resp in ("s", "sim", "y", "yes"):
                return True
            if resp in ("n", "nao", "não", "no"):
                return False
            print("Resposta inválida. Digite S ou N.")
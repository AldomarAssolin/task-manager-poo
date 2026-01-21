"""
Docstring para src.application.ports.confirmacao_ui

Porta (interface) para confirmação do usuário.
O caso de uso não depende de input/print direto.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

class IConfirmacaoUI(ABC):
    @abstractmethod
    def confirmar(self, pergunta: str) -> bool:
        raise NotImplementedError
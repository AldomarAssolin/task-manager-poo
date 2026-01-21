"""

Docstring para src.domain.erros

erros.py

Erros de domínio padronizados (controle explícito, sem exceptions).
"""

from __future__ import annotations

from src.domain.resultado import ErroDominio

def titulo_invalido() -> ErroDominio:
    return ErroDominio(
        codigo="TITULO_INVALIDO",
        mensagem="Título inválido. Informe um título não vazio."
    )
      
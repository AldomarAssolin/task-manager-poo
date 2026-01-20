"""
Docstring para src.domain.resultado

resultado.py

Objeto Resultado (Result) para controle explícito de fluxo:
- Sucesso: carrega um valor
- Falha: carrega um erro de domínio


"""

from __future__ import annotations
from typing import Generic, TypeVar, Union
from dataclasses import dataclass

T = TypeVar("T")

@dataclass(frozen=True)
class ErroDominio:
    """
    Representa um erro do domínio (regras de negócio).

    - codigo: identificador curto e estável (para logs e testes)
    - mensagem: texto amigável para exibir ao usuário
    """
    codigo: str
    mensagem: str
    
    def __str__(self) -> str:
        return f"[{self.codigo}] {self.mensagem}"
    
@dataclass(frozen=True)
class Resultado(Generic[T]):
    """
    Representa o resultado de uma operação que pode falhar.

    Regras:
    - Se sucesso=True: valor deve existir e erro deve ser None
    - Se sucesso=False: erro deve existir e valor deve ser None
    """
    sucesso: bool
    valor: Union[T, None] = None
    erro: Union[ErroDominio, None] = None

    @staticmethod
    def ok(valor: T) -> "Resultado[T]":
        """Cria um resultado de sucesso"""
        return Resultado(sucesso=True, valor=valor, erro=None)

    @staticmethod
    def falha(erro: ErroDominio) -> "Resultado[T]":
        """Cria um resultado de falha"""
        return Resultado(sucesso=False, valor=None, erro=erro)
    
    def is_ok(self) -> bool:
        """Verifica se o resultado é de sucesso"""
        return self.sucesso
    
    def is_falha(self) -> bool:
        """Verifica se o resultado é de falha"""
        return not self.sucesso
    
    def obter_valor(self) -> T:
        """
        Retorna o valor se for sucesso.

        Observação:
        Aqui eu lanço exceção porque é erro de programação (bug),
        não regra de negócio. Você tentou ler valor de uma falha.
        """
        if not self.sucesso or self.valor is None:
            raise ValueError("Tentativa de obter valor de um Resultado de falha.")
        return self.valor
    
    def obter_erro(self) -> ErroDominio:
        """
        Retorna o erro se for falha.

        Mesma lógica: exceção aqui indica bug no código chamador.
        """
        if self.sucesso or self.erro is None:
            raise ValueError("Tentativa de obter erro de um Resultado de sucesso.")
        return self.erro
"""
Docstring para src.domain.repositorio_tarefa

Contrato (interface) do repositório de tarefas.
A infra (memória, CSV, SQLite) implementa esse contrato.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.tarefa import Tarefa

class IRepositorioTarefa(ABC):
    @abstractmethod
    def adicionar(self, tarefa: Tarefa) -> None:
        raise NotImplementedError

    @abstractmethod
    def atualizar(self, tarefa: Tarefa) -> None:
        raise NotImplementedError

    @abstractmethod
    def remover(self, tarefa_id: UUID) -> Optional[Tarefa]:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, tarefa_id: UUID) -> Optional[Tarefa]:
        raise NotImplementedError
    
    @abstractmethod
    def buscar_por_titulo_normalizado(self, titulo_norm: str) -> Optional[Tarefa]:
        raise NotImplementedError
    
    @abstractmethod
    def listar(self) -> List[Tarefa]:
        raise NotImplementedError
"""
Docstring para src.infrastructure.repositories.repositorio_memoria

Repositório em memória para tarefas.
Implementa IRepositorioTarefas usando um dict por id.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from uuid import UUID

from src.domain.tarefa import Tarefa
from src.domain.repositorio_tarefa import IRepositorioTarefa

class RepositorioTarefasEmMemoria(IRepositorioTarefa):
    def __init__(self) -> None:
        self._itens: Dict[UUID, Tarefa] = {}
        
    def adicionar(self, tarefa: Tarefa) -> None:
        self._itens[tarefa.id] = tarefa
        
    def atualizar(self, tarefa: Tarefa) -> None:
        self._itens[tarefa.id] = tarefa
        
    def remover(self, tarefa_id: UUID) -> None:
        if tarefa_id in self._itens:
            del self._itens[tarefa_id]
            
    def buscar_por_id(self, tarefa_id: UUID) -> Optional[Tarefa]:
        return self._itens.get(tarefa_id)
    
    def buscar_por_titulo_normalizado(self, titulo_norm: str) -> Optional[Tarefa]:
        # Busca linear (em memória e poucos itens).
        # Depois otimizar com índice por titulo_norm.
        titulo_norm = (titulo_norm or "").casefold().strip()
        
        for tarefa in self._itens.values():
            if tarefa.titulo_normalizado == titulo_norm:
                return tarefa
        return None
    
    def listar(self) -> List[Tarefa]:
        return list(self._itens.values())
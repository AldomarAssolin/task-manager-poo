"""
Docstring para src.application.dto.adicionar_tarefa_dto

DTOs (Command/Result) do UC01 - Adicionar Tarefa.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.domain.tarefa import Tarefa

@dataclass(frozen=True) 
class AdicionarTarefaCommand:
    titulo: str
    descricao: str = ""
    
    
@dataclass(frozen=True)
class AdicionarTarefaResultado:
    criada: bool
    atualizada: bool
    cancelada: bool
    mensagem: str
    tarefa: Optional[Tarefa] = None
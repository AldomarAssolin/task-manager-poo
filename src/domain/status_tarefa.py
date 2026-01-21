"""
Docstring para src.domain.status_tarefa

Enum para status da tarefa.
"""


from enum import Enum

class StatusTarefa(str, Enum):
    PENDENTE = "PENDENTE"
    CONCLUIDA = "CONCLUIDA"
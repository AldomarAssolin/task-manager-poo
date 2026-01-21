"""
Docstring para src.domain.tarefa

Entidade Tarefa (Domínio).
- Criação via método de fábrica: Tarefa.criar(...)
- Normalização do título dentro da entidade
- Atualização de descrição ignora valores vazios (regra RN-UC01-03)
- Controle explícito: retorna Resultado[Tarefa]

"""

from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.domain.status_tarefa import StatusTarefa
from src.domain.resultado import Resultado, ErroDominio
from src.domain.erros import titulo_invalido

def _agora_utc() -> datetime:
    return datetime.now(timezone.utc)

def _is_blank(valor: Optional[str]) -> bool:
    return valor is None or valor.strip() == ""

@dataclass(frozen=False)
class Tarefa:
    
    _id: UUID
    _titulo: str
    _titulo_normalizado: str
    _descricao: str
    _status: StatusTarefa
    _criada_em: datetime
    _atualizada_em: datetime
    
    @classmethod
    def criar(cls, titulo:str, descricao: str = "") -> Resultado["Tarefa"]:
        titulo_limpo = cls._normalizar_titulo_exibicao(titulo)
        titulo_norm = cls._normalizar_titulo_comparacao(titulo_limpo)
        
        if _is_blank(titulo_limpo):
            return Resultado.falha(titulo_invalido())
        
        agora = _agora_utc()
        tarefa = cls(
            _id=uuid4(),
            _titulo=titulo_limpo,
            _titulo_normalizado = titulo_norm,
            _descricao=descricao.strip() if descricao is not None else "",
            _status=StatusTarefa.PENDENTE,
            _criada_em=agora,
            _atualizada_em=agora
        )
        return Resultado.ok(tarefa)
    
    # -------------- Propriedades (getters) --------------
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def titulo(self) -> str:
        return self._titulo
    
    @property
    def titulo_normalizado(self) -> str:
        return self._titulo_normalizado
    
    @property
    def descricao(self) -> str:
        return self._descricao
    
    @property
    def status(self) -> StatusTarefa:
        return self._status
    
    @property
    def criada_em(self) -> datetime:
        return self._criada_em
    
    @property
    def atualizada_em(self) -> datetime:
        return self._atualizada_em
    
    # -------------- Comportamentos --------------
    def atualizar_descricao(self, nova_descricao: Optional[str]) -> None:
        """
        RN-UC01-03: descrição vazia/nula NÃO altera a descrição existente.
        """
        if _is_blank(nova_descricao):
            return
        
        self._descricao = nova_descricao.strip()
        self.touch()
        
    def marcar_concluida(self) -> None:
            self._status = StatusTarefa.CONCLUIDA
            self.touch()
            
    def marcar_pendente(self) -> None:
            self._status = StatusTarefa.PENDENTE
            self.touch()
            
    def touch(self) -> None:
        """
        Atualiza a data de atualização.

        Útil para o UC01 quando o usuário confirma "atualizar"
        mas a descrição veio vazia e foi preservada.
        O service pode chamar touch() explicitamente nesse caso.
        """
        
        self._atualizada_em = _agora_utc()
        
    # -------------- Normalizacaoes --------------
    @staticmethod
    def _normalizar_titulo_exibicao(valor: str) -> str:
        """
        Normaliza para guardar como título exibível:
        - strip nas pontas
        - colapsa múltiplos espaços internos para 1
        """
        if valor is None:
            return ""
        
        partes = valor.strip().split()
        return " ".join(partes)
    
    @staticmethod
    def _normalizar_titulo_comparacao(valor: str) -> str:
        """
        Normaliza para comparação:
        - case-insensitive (casefold)
        """
        
        return valor.casefold()
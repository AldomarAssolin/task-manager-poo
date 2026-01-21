"""
Docstring para src.application.services.adicionar_tarefa_service

UC01 - Adicionar Tarefa

Regras aplicadas:
- Criação de tarefa via Tarefa.criar(...) (normaliza/valida no domínio)
- Duplicidade por titulo_normalizado
- Se duplicado: perguntar se quer atualizar descrição
- Se confirmou e descrição vazia: não altera descrição (RN-UC01-03)
"""

from __future__ import annotations

from src.application.dto.adicionar_tarefa_dto import (
    AdicionarTarefaCommand,
    AdicionarTarefaResultado,
)
from src.application.ports.confirmacao_ui import IConfirmacaoUI
from src.domain.resultado import Resultado
from src.domain.tarefa import Tarefa
from src.domain.repositorio_tarefa import IRepositorioTarefa


class AdicionarTarefaService:
    def __init__(sel, repo: IRepositorioTarefa, ui_confirmacao: IConfirmacaoUI) -> None:
        sel._repo = repo
        sel._ui_confirmacao = ui_confirmacao
        
    def executar(self, cmd: AdicionarTarefaCommand) -> Resultado[AdicionarTarefaResultado]:
        
        # 1) Validar/criar "candidata" via domínio (controle explícito)

        r_tarefa = Tarefa.criar(cmd.titulo, cmd.descricao)
        if r_tarefa.is_falha():
            erro = r_tarefa.obter_erro()
            return Resultado.falha(erro)
        
        candidata = r_tarefa.obter_valor()
        
        # 2) Verificar duplicidade por título normalizado
        existente = self._repo.buscar_por_titulo_normalizado(
            candidata.titulo_normalizado
        )
        
        if existente is None:
            # Não existe: adicionar nova
            self._repo.adicionar(candidata)
            res = AdicionarTarefaResultado(
                criada=True,
                atualizada=False,
                cancelada=False,
                tarefa=candidata,
                mensagem="Tarefa criada com sucesso.",
            )
            return Resultado.ok(res)
        
        # 4) Se duplicado: perguntar se deseja atualizar descrição
        
        pergunta = (
            f"Já existe uma tarefa com o título '{existente.titulo}'. "
            "Deseja atualizar a descrição da existente? (S/N)"
        )
        confirmar = self._ui_confirmacao.confirmar(pergunta)
        
        if not confirmar:
            # Usuário não confirmou atualização
            res = AdicionarTarefaResultado(
                criada=False,
                atualizada=False,
                cancelada=True,
                tarefa=existente,
                mensagem="Operação cancelada. Nenhuma tarefa foi alterada.",
            )
            return Resultado.ok(res)

        # 5) Confirmou: atualizar SOMENTE descrição (RN-UC01-02)
        desc_antes = existente.descricao
        existente.atualizar_descricao(cmd.descricao)
        
        # Mesmo se a descrição vier vazia e for preservada, registramos atualização
        # (definido no UC01).
        
        if existente.descricao == desc_antes:
            existente.touch()  # Atualiza timestamp mesmo sem mudança de descrição
            
        self._repo.atualizar(existente)
        
        mensagem = (
            "Descrição atualizada com sucesso."
            if existente.descricao != desc_antes
            else "Nenhuma alteração aplicada na descrição."
        )
        
        res = AdicionarTarefaResultado(
            criada=False,
            atualizada=True,
            cancelada=False,
            tarefa=existente,
            mensagem=mensagem,
        )
        return Resultado.ok(res)
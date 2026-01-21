from src.application.dto.adicionar_tarefa_dto import AdicionarTarefaCommand
from src.application.services.adicionar_tarefa_service import AdicionarTarefaService
from src.infrastructure.repositories.repositorio_memoria import RepositorioTarefasEmMemoria
from src.interface.cli.confirmacao_ui_cli import ConfirmacaoUICLI


def main() -> None:
    repo = RepositorioTarefasEmMemoria()
    ui = ConfirmacaoUICLI()
    service = AdicionarTarefaService(repo, ui)

    # 1) cria
    r1 = service.executar(AdicionarTarefaCommand("Estudar Python", "POO + RUP"))
    print(r1.obter_valor().mensagem if r1.is_ok() else r1.obter_erro())

    # 2) tenta duplicado
    r2 = service.executar(AdicionarTarefaCommand("  estudar   python  ", "Nova descrição aqui"))
    if r2.is_ok():
        print(r2.obter_valor().mensagem)
    else:
        print(r2.obter_erro())

    # 3) listar no final
    print("\n== Tarefas ==")
    for t in repo.listar():
        print(f"- {t.titulo} | {t.status} | {t.descricao}")


if __name__ == "__main__":
    main()

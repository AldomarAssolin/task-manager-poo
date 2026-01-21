
from src.domain.resultado import Resultado, ErroDominio
from src.domain.tarefa import Tarefa



def main() -> None:
    
    r = Tarefa.criar("  Estudar   Python  ", "Ver POO e RUP")
    if r.is_falha():
        print("Erro:", r.obter_erro())
        return

    tarefa = r.obter_valor()
    print("OK:", tarefa.titulo, "| norm:", tarefa.titulo_normalizado)

    tarefa.atualizar_descricao("   ")  # deve IGNORAR
    tarefa.touch()  # se quiser registrar atualização mesmo sem mudar nada
    print("Descrição:", tarefa.descricao)
    
if __name__ == "__main__":
    main()
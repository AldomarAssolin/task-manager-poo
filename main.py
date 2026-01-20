
from src.domain.resultado import Resultado, ErroDominio


def dividir(a: int, b: int) -> Resultado[float]:
    if b == 0:
        return Resultado.falha(ErroDominio("DIVISAO_POR_ZERO", "Não dá pra dividir por zero."))
    return Resultado.ok(a / b)



def main() -> None:
    
    r1 = dividir(10, 2)
    if r1.is_ok():
        print("Sucesso:", r1.obter_valor())
    else:
        print("Erro:", r1.obter_erro())

    r2 = dividir(10, 0)
    if r2.is_ok():
        print("Sucesso:", r2.obter_valor())
    else:
        print("Erro:", r2.obter_erro())
    
if __name__ == "__main__":
    main()
from banco.faturamentos import faturamento_semana

def calcular_reserva():
    faturamentos = faturamento_semana()

    return faturamentos * 0.20


def calcular_lucro():
    faturamentos = faturamento_semana()
    reserva = calcular_reserva()

    return faturamentos - reserva
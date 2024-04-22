from matplotlib import pyplot as plt
import scipy
from limpar_tela import LimparTela
from tratamento_de_dados import TratarDados
from visualizacao_de_dados import VisualizarDados

limpar_tela = LimparTela()

limpar_tela.limpar_tela()

Tempo, Degrau, Temperatura, dataset = TratarDados().tratar_dados()

VisualizarDados().visualizar(Tempo, Degrau, Temperatura, dataset)

valorFinal = Temperatura[-1]
amplitudeDegrau = Degrau[-1]
ganhoEstatico = valorFinal / amplitudeDegrau
print(f"  - O Ganho Estático do Sistema é k = {ganhoEstatico:.4f}.\n\n")

atrasoTransporte = 0
constanteTempo = 0
for i, temp in enumerate(Temperatura):
    if temp != 0 and atrasoTransporte == 0:
        atrasoTransporte = Tempo[i - 1]
        print(f"O Atraso de Transporte do Sistema é T = {atrasoTransporte:.2f}.")
    if temp >= (0.6321 * valorFinal):
        constanteTempo = Tempo[i] - atrasoTransporte
        print(f"A Constante de Tempo do Sistema é t = {constanteTempo:.2f}.\n")
        break

# Modelo para um Sistema de Primeira Ordem com Atraso de Transporte
print("Função de Transferência do Modelo:")
numerator = [ganhoEstatico]
denominator = [constanteTempo, 1]
sys = (numerator, denominator)
print(sys)

# Relatório 8: Sintonia de Controladores PID
# Método 1: Ziegler Nichols Malha Aberta - ZNMA
print("\nFunção de Transferência para o Controlador PID ZNMA:")
Kp = 1.2 * constanteTempo / (ganhoEstatico * atrasoTransporte)
Ti = 2 * atrasoTransporte
Td = atrasoTransporte / 2
print(f"Kp = {Kp:.4f}")
print(f"Ti = {Ti:.4f}")
print(f"Td = {Td:.4f}")

from control import TransferFunction

numerator = [Kp * Td, Kp, Kp / Ti]
denominator = [1, 0]
PID = TransferFunction(numerator, denominator)
print("Função de Transferência do PID:")
print(PID)


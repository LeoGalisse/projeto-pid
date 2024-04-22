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


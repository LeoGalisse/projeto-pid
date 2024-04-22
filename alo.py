import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import control as cnt

# ----------------------------------------------------------------------------
# Relatório 1: Introdução ao Python.
# - Tema: Importação dos Dados.
# - Procedimento: Para Importar um Conjunto de Dados, especifique o caminho do
# arquivo .mat na função 'np.load'.
# ----------------------------------------------------------------------------
# Especifique o caminho do arquivo .mat.
data = loadmat('Dataset_Grupo2.mat')

# Extração dos dados do arquivo .mat.
tempo = data['TARGET_DATA____ProjetoC213_Degrau'][:, 0]
degrau = data['TARGET_DATA____ProjetoC213_Degrau'][:, 1]
temperatura = data['TARGET_DATA____ProjetoC213_Saida'][:, 2]

# ----------------------------------------------------------------------------
# Relatório 2: Vetores e Matrizes.
# - Tema: Tratamento dos Dados.
# - Procedimento: Analisar as Matrizes e separar em Vetores.
# ----------------------------------------------------------------------------
# Análise dos dados:
# Verificar se os dados estão organizados como vetores ou matrizes.
if degrau.ndim == 1:  # Os dados são organizados como vetores.
    degrau = degrau
    temperatura = temperatura
else:  # Os dados são organizados como matrizes.
    degrau = degrau[:, 0]
    temperatura = temperatura[:, 0]

# ----------------------------------------------------------------------------
# Relatório 3: Plotagem de Gráficos 2D.
# - Tema: Visualização do Conjunto de Dados.
# - Procedimento: Plotar os Gráficos do Degrau e Temperatura ao longo do Tempo.
# ----------------------------------------------------------------------------
# Plotando os gráficos.
plt.figure()
plt.plot(tempo, degrau, label='Degrau')
plt.plot(tempo, temperatura, label='Temperatura')
plt.xlabel('Tempo (segundos)')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.title('Trabalho Prático C213\nIdentificação de Sistemas de Controle')
plt.grid(True)
plt.savefig('dataset_plot.png')
plt.show()

# ----------------------------------------------------------------------------
# Relatório 4: Resposta Típica de Sistemas de Primeira Ordem.
# - Tema: Caracterização do Conjunto de Dados.
# - Procedimento: Calcular o Ganho Estático do Sistema - k.
# ----------------------------------------------------------------------------
# Cálculo do Ganho Estático.
valor_final = temperatura[-1]
amplitude_degrau = degrau[-1]
ganho_estatico = valor_final / amplitude_degrau
print(f'O Ganho Estático do Sistema é k = {ganho_estatico:.4f}.')

# ----------------------------------------------------------------------------
# Relatório 6: Atraso de Transporte.
# - Tema: Caracterização do Conjunto de Dados.
# - Procedimento: Calcular o Atraso de Transporte - T.
# ----------------------------------------------------------------------------
# Cálculo do Atraso de Transporte.
atraso_transporte = 0
constante_tempo = 0
for i in range(len(temperatura)):
    if temperatura[i] != 0 and atraso_transporte == 0:
        atraso_transporte = tempo[i - 1]
        print(f'O Atraso de Transporte do Sistema é T = {atraso_transporte:.2f}.')

    if temperatura[i] >= (0.6321 * valor_final):
        constante_tempo = tempo[i] - atraso_transporte
        print(f'A Constante de Tempo do Sistema é t = {constante_tempo:.2f}.\n')
        break

# Modelo para um Sistema de Primeira Ordem com Atraso de Transporte:
print('Função de Transferência do Modelo:')
print(f'G(s) = {ganho_estatico} / (τs + 1) * exp(-Ts)')

# Convertendo os dados degrau e temperatura para arrays unidimensionais
if degrau.ndim > 1:
    degrau = degrau[:, 0]
if temperatura.ndim > 1:
    temperatura = temperatura[:, 0]

# Definindo a função de transferência em malha aberta
k = 2
tau = 3
num = np.array([k])
den = np.array([tau, 1])
H = cnt.tf(num, den)

Theta = 2
n_pade = 20
(num_pade, den_pade) = cnt.pade(Theta, n_pade)
H_pade = cnt.tf(num_pade, den_pade)

# Parâmetros do controlador PID
kp = 3.6
Ti = 1
Td = 0.25

# Controlador proporcional
numkp = np.array([kp])
denkp = np.array([1])
Hkp = cnt.tf(numkp, denkp)

# Controlador integral
numki = np.array([kp])
denki = np.array([Ti, 0])
Hki = cnt.tf(numki, denki)

# Controlador derivativo
numkd = np.array([kp * Td, 0])
denkd = np.array([1])
Hkd = cnt.tf(numkd, denkd)

# Juntando todos os blocos
Hctrl1 = cnt.parallel(Hkp, Hki)
Hctrl = cnt.parallel(Hctrl1, Hkd)
Hs = cnt.series(H, H_pade)
Hdel = cnt.series(Hs, Hctrl)
Hcl = cnt.feedback(Hdel, 1)

# Plotando a resposta ao degrau
t = np.linspace(0, 0.5, 100)
t, y = cnt.step_response(Hcl, t)
plt.plot(t, y, label="Resposta ao Degrau")
plt.xlabel('Tempo [s]')
plt.ylabel('Temperatura [°C]')
plt.title('Resposta ao Degrau - Malha Aberta')
plt.grid()
plt.legend()
plt.xlim(0, tempo[-1])  # Limitando o eixo x ao tempo máximo do dataset
plt.ylim(0, max(max(degrau), max(temperatura)) * 1.05)  # Limitando o eixo y
plt.show()
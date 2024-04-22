import numpy as np
import control as cnt
import matplotlib.pyplot as plt
from scipy.io import loadmat

# Carregar dados do arquivo .mat
data = loadmat('Dataset_Grupo2.mat')

# Extrair dados do degrau e da saída
degrau_data = data['TARGET_DATA____ProjetoC213_Degrau']
saida_data = data['TARGET_DATA____ProjetoC213_Saida']

# Extrair o tempo e a saída do degrau
tempo_degrau = degrau_data[0].flatten()
saida_degrau = degrau_data[1].flatten()

# Tempo total de simulação (em segundos)
tempo_simulacao = 420

# Parâmetros do controlador PID
kp = 2
Ti = 4
Td = 1

# Função de transferência do processo
k = saida_data[1][-1]
tau = tempo_degrau[np.where(np.abs(saida_degrau - saida_degrau[-1]) < 0.02 * saida_degrau[-1])[0][-1]]
num = np.array([k])
den = np.array([tau, 1])
H = cnt.tf(num, den)

# Função de transferência do controlador proporcional (P)
numkp = np.array([kp])
denkp = np.array([1])
Hkp = cnt.tf(numkp, denkp)

# Função de transferência do controlador integral (I)
numki = np.array([kp])
denki = np.array([Ti, 0])
Hki = cnt.tf(numki, denki)

# Função de transferência do controlador derivativo (D)
numkd = np.array([kp*Td, 0])
denkd = np.array([1])
Hkd = cnt.tf(numkd, denkd)

# Função de transferência do controlador PID
Hctrl1 = cnt.parallel(Hkp, Hki)
Hctrl = cnt.parallel(Hctrl1, Hkd)

# Função de transferência em malha aberta
Hs = cnt.series(Hctrl, H)

# Função de transferência em malha fechada
Hcl = cnt.feedback(Hs, 1)

# Simular a resposta ao degrau
t = np.linspace(0, tempo_simulacao, 1000)
t, y = cnt.step_response(Hcl, T=t)

# Plotar a resposta
plt.plot(t, y, label="kp=2, Ti=4, Td=1")
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.title('Resposta ao Degrau do Sistema em Malha Fechada')
plt.legend(title='Curvas')
plt.grid()
plt.show()

# Extrair o tempo e a saída do degrau
tempo_degrau = degrau_data[0].flatten()
saida_degrau = degrau_data[1].flatten()

# Tempo total de simulação (em segundos)
tempo_simulacao = 420

# Parâmetros do controlador PID
kp = 2
Ti = 1
Td = 0.5

# Função de transferência do processo
k = saida_data[1][-1]
tau = tempo_degrau[np.where(np.abs(saida_degrau - saida_degrau[-1]) < 0.02 * saida_degrau[-1])[0][-1]]
num = np.array([k])
den = np.array([tau, 1])
H = cnt.tf(num, den)

# Função de transferência do controlador PID
numkp = np.array([kp])
denkp = np.array([1])
Hkp = cnt.tf(numkp, denkp)

numki = np.array([kp])
denki = np.array([Ti, 0])
Hki = cnt.tf(numki, denki)

numkd = np.array([kp*Td, 0])
denkd = np.array([1])
Hkd = cnt.tf(numkd, denkd)

# Função de transferência do controlador PID
Hctrl1 = cnt.parallel(Hkp, Hki)
Hctrl = cnt.parallel(Hctrl1, Hkd)

# Função de transferência em malha aberta
Hs = cnt.series(Hctrl, H)

# Simular a resposta ao degrau em malha aberta
t = np.linspace(0, tempo_simulacao, 1000)
t, y = cnt.step_response(Hs, T=t)

# Plotar a resposta
plt.plot(t, y)
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.title('Resposta ao Degrau em Malha Aberta com PID')
plt.grid()
plt.show()

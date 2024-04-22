from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt

# Função para simular a resposta do sistema com os parâmetros identificados
def simular_resposta(k, theta, tau, tempo_simulacao):
    # Tempo de amostragem
    dt = 0.01
    # Vetor de tempo
    t = np.arange(0, tempo_simulacao, dt)
    
    # Simulação da resposta do sistema
    # Vamos usar uma função de transferência de primeira ordem para simplificar
    y_real = k * (1 - np.exp(-(t - theta) / tau))
    
    return t, y_real

# Função para identificar os parâmetros k, theta e tau usando o Método de Identificação da Planta - Smith
def identificar_planta_smith(degrau_data, saida_data):
    # A identificação de parâmetros pode variar dependendo dos dados e da natureza do sistema.
    # Aqui vou fornecer um exemplo básico de identificação de parâmetros usando a resposta ao degrau.

    # Extrair o tempo e a saída do degrau
    tempo_degrau = degrau_data[0]
    saida_degrau = degrau_data[1]

    # Tempo de atraso (tempo até a saída começar a se mover)
    theta = tempo_degrau[np.where(saida_degrau > 0)[0][0]]

    # Tempo do pico da resposta ao degrau
    T_p = tempo_degrau[np.argmax(saida_degrau)]

    # Tempo de estabilização (tempo para que a resposta fique dentro de uma faixa de tolerância em torno do valor final)
    T_s = tempo_degrau[np.where(np.abs(saida_degrau - saida_degrau[-1]) < 0.02 * saida_degrau[-1])[0][-1]]

    # Overshoot máximo (em porcentagem do valor final)
    M_p = (np.max(saida_degrau) - saida_degrau[-1]) / saida_degrau[-1] * 100

    # Valor final (considerado igual ao valor final da resposta ao degrau)
    k = saida_data[1][-1]

    # Calcular os parâmetros do modelo
    k_identificado = M_p
    theta_identificado = 0  # Supondo que não há tempo de atraso
    tau_identificado = T_s - T_p

    return k_identificado, theta_identificado, tau_identificado

# Carregar dados do arquivo .mat
data = loadmat('Dataset_Grupo2.mat')

# Extrair dados do degrau e da saída
degrau_data = data['TARGET_DATA____ProjetoC213_Degrau']
saida_data = data['TARGET_DATA____ProjetoC213_Saida']

# Identificar os parâmetros usando o Método de Identificação da Planta - Smith
k_identificado, theta_identificado, tau_identificado = identificar_planta_smith(degrau_data, saida_data)

# Simular a resposta do sistema com os parâmetros identificados
tempo_simulacao = 420  # Tempo total de simulação (em segundos)
t, y_estimada = simular_resposta(k_identificado, theta_identificado, tau_identificado, tempo_simulacao)

# Plotar os resultados
plt.figure(figsize=(10, 6))
plt.plot(degrau_data[0], saida_data[1], label='Resposta Original')
plt.plot(t, y_estimada, label='Resposta Estimada')
plt.title('Comparação entre Resposta Original e Estimada')
plt.xlabel('Tempo (s)')
plt.ylabel('Saída do Sistema')
plt.legend()
plt.grid(True)
plt.show()

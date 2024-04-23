from limpar_tela import LimparTela
from tratamento_de_dados import TratarDados
from visualizacao_de_dados import VisualizarDados
import matplotlib.pyplot as plt
import control as ctl
import numpy as np

# Clear the screen
limpar_tela = LimparTela()
limpar_tela.limpar_tela()

# Load dataset and process data
Tempo, Degrau, Temperatura, dataset = TratarDados().tratar_dados()

# Visualize data
VisualizarDados().visualizar(Tempo, Degrau, Temperatura, dataset)

# Calculate static gain
valorFinal = Temperatura[-1]
amplitudeDegrau = Degrau[-1]

# Check if amplitudeDegrau is zero, handle this case appropriately
if amplitudeDegrau == 0:
    print("Error: Amplitude degrau é zero, não é possível calcular o ganho estático.")
    exit()

ganhoEstatico = valorFinal / amplitudeDegrau
print(f"  - O Ganho Estático do Sistema é k = {ganhoEstatico:.4f}.\n\n")

# Calculate transport delay and time constant
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

# Check if constanteTempo is negative or zero
if constanteTempo <= 0:
    print("Error: Constante de tempo é negativa ou zero, verifique os dados de entrada.")
    print(f"constanteTempo: {constanteTempo}")
    print(f"Temperatura: {Temperatura}")
    print(f"Tempo: {Tempo}")
    exit()

# Calculate PID controller parameters using Internal Model Control method (IMC)
print('\nFunção de Transferência para o Controlador PID IMC:\n')
_lambda = 75
Kp = (2 * constanteTempo + atrasoTransporte) / (ganhoEstatico * (2 * _lambda + atrasoTransporte))
Td = constanteTempo * atrasoTransporte / (2 * constanteTempo + atrasoTransporte)
Ti = constanteTempo + atrasoTransporte / 2
print(f'  - Kp = {Kp:.4f}\n  - Ti = {Ti:.4f}\n  - Td = {Td:.4f}\n')

# Define PID controller transfer function using IMC method
numerator = [Kp * Td, Kp, Kp / Ti]
denominator = [1, 0]
PID = ctl.TransferFunction(numerator, denominator)

# Define system transfer function
numerator_sys = [1]
denominator_sys = [1, 2, 1]
sys = ctl.TransferFunction(numerator_sys, denominator_sys)

# Plot step response
t, y = ctl.step_response(ctl.feedback(PID * sys))
plt.figure()
plt.plot(t, y)
plt.title('Resposta ao degrau')
plt.xlabel('Tempo')
plt.ylabel('Amplitude')
plt.grid()
plt.show()


# Calculate PID controller parameters
print('\nFunção de Transferência para o Controlador PID CHR sem overshoot:\n')
Kp = 0.6 * constanteTempo / (ganhoEstatico * atrasoTransporte)

# Check if Kp is valid, handle this case appropriately
if np.isinf(Kp) or np.isnan(Kp):
    print("Error: Kp é inválido, verifique os dados de entrada.")
    exit()

Ti = constanteTempo
Td = atrasoTransporte / 2
print(f'  - Kp = {Kp:.4f}\n  - Ti = {Ti:.4f}\n  - Td = {Td:.4f}\n')

# Define PID controller transfer function
numerator = [Kp*Td, Kp, Kp/Ti]
denominator = [1, 0]
PID = ctl.TransferFunction(numerator, denominator)

# Define system transfer function
numerator_sys = [1]
denominator_sys = [1, 2, 1]
sys = ctl.TransferFunction(numerator_sys, denominator_sys)

# Plot step response
t, y = ctl.step_response(ctl.feedback(PID * sys))
plt.figure()
plt.plot(t, y)
plt.title('Resposta ao degrau')
plt.xlabel('Tempo')
plt.ylabel('Amplitude')
plt.grid()
plt.show()

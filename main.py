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

theta = Tempo[np.argmax(np.abs(Temperatura) > 0.05)]  # Find the time at which the response starts to change
tau = Tempo[np.argmax(Temperatura >= 0.632 * Temperatura[-1])] - theta  # Find the time constant tau

# Calculate the static gain (k) of the system
k = Temperatura[-1] / Degrau[-1]

theta += atrasoTransporte

# Print the identified parameters
print(f"Identified Parameters:")
print(f"  - Gain (k): {k:.4f}")
print(f"  - Time Delay (θ): {theta:.4f}")
print(f"  - Time Constant (τ): {tau:.4f}")

# Define the transfer function based on the identified parameters
numerator = [k]
denominator = [tau, 1]  # First-order system with time delay
sys = ctl.TransferFunction(numerator, denominator) * ctl.TransferFunction([1], [1, 0, 1])

# Plot the step response of the identified model
t, y = ctl.step_response(sys)
plt.figure()
plt.plot(t, y)
plt.title('Identified System Step Response')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.grid()
plt.show()

# Plot original and estimated step responses
plt.figure()
plt.plot(t, y, label='Estimated Response')
plt.plot(Tempo, Temperatura, label='Original Response')
plt.title('Comparison of Original and Estimated Step Responses')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.grid()
plt.show()

# Fine-tuning parameters
# Experiment with adjusting parameters (k, theta, tau) to improve the fit
# You can manually adjust the parameters or use optimization techniques to find the best fit

# Example of manual fine-tuning:
# k = k * 1.1  # Increase the gain by 10%
# theta = theta * 1.05  # Increase the time delay by 5%
# tau = tau * 0.95  # Decrease the time constant by 5%

# Define the transfer function with the updated parameters
numerator = [k]
denominator = [tau, 1]  # First-order system with time delay
sys = ctl.TransferFunction(numerator, denominator) * ctl.TransferFunction([1], [1, 0, 1])

# Plot the updated estimated step response
t, y = ctl.step_response(sys)
plt.figure()
plt.plot(t, y, label='Updated Estimated Response')
plt.plot(Tempo, Temperatura, label='Original Response')
plt.title('Comparison of Original and Updated Estimated Step Responses')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.grid()
plt.show()

# Define PID controller parameters for both open-loop and closed-loop systems
# Estimativa inicial dos parâmetros do controlador PID
Kp = 1.0
Ti = 1.0
Td = 0.5

# Open-loop (no feedback)
Kp_open = Kp
Ti_open = Ti
Td_open = Td
numerator_open = [Kp_open * Td_open, Kp_open, Kp_open / Ti_open]
denominator_open = [1, 0]
PID_open = ctl.TransferFunction(numerator_open, denominator_open)

# Closed-loop (feedback)
Kp_closed = Kp
Ti_closed = Ti
Td_closed = Td
numerator_closed = [Kp_closed * Td_closed, Kp_closed, Kp_closed / Ti_closed]
denominator_closed = [1, 0]
PID_closed = ctl.TransferFunction(numerator_closed, denominator_closed)

# Define system transfer function
numerator_sys = [1]
denominator_sys = [1, 2, 1]
sys = ctl.TransferFunction(numerator_sys, denominator_sys)

# Simulate open-loop system
sys_open = sys * PID_open
t_open, y_open = ctl.step_response(sys_open)

# Simulate closed-loop system
feedback_sys = ctl.feedback(PID_closed * sys)
t_closed, y_closed = ctl.step_response(feedback_sys)

# Plot step responses
plt.figure()
plt.plot(t_open, y_open, label='Open Loop')
plt.plot(t_closed, y_closed, label='Closed Loop')
plt.title('Step Response Comparison')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.grid()
plt.show()


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

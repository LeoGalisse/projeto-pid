import matplotlib.pyplot as plt
import numpy as np

class VisualizarDados:
    def __init__(self):
        pass

    def visualizar(self, Tempo, Degrau, Temperatura, dataset):
      plt.figure()
      plt.plot(Tempo, Degrau, label='Degrau')
      plt.plot(Tempo, Temperatura, label='Temperatura')
      plt.xlabel('Time (seconds)')
      plt.ylabel('Temperatura [°C]')
      plt.legend(loc='upper left')
      plt.xlim([0, Tempo[-1]])
      plt.ylim([0, max(np.max(Degrau), np.max(Temperatura)) * 1.05])
      plt.title('Identificação de Sistemas de Controle\n')
      plt.grid(True)
      plt.savefig(dataset + '.png')
      plt.show()
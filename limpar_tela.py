import os
import matplotlib.pyplot as plt
class LimparTela:
    def __init__(self):
        self.os = os
        self.plt = plt

    def limpar_tela(self):
        self.os.system('cls' if self.os.name == 'nt' else 'clear')
        self.plt.close('all')
        print()
        return
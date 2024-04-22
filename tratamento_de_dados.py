from importar_dados import ImportarDados

class TratarDados:
  def __init__(self):
    pass

  def tratar_dados(self):
    mat_contents, file_name = ImportarDados().importar_dados()

    if mat_contents is None:
        print("Nenhum arquivo .mat selecionado. A execução será encerrada.")
        exit()

    TARGET_DATA_PrimeiraOr_Degrau = mat_contents['TARGET_DATA____ProjetoC213_Degrau']
    TARGET_DATA_PrimeiraOr_Saida = mat_contents['TARGET_DATA____ProjetoC213_Saida']

    shape_Degrau = TARGET_DATA_PrimeiraOr_Degrau.shape
    shape_Saida = TARGET_DATA_PrimeiraOr_Saida.shape

    if shape_Degrau[0] < shape_Degrau[1]:  # As matrizes são do tipo Coluna.
        Tempo = TARGET_DATA_PrimeiraOr_Degrau[:, 0]
        Degrau = TARGET_DATA_PrimeiraOr_Degrau[:, 1]
        Temperatura = TARGET_DATA_PrimeiraOr_Saida[:, 1]
    else:  # As matrizes são do tipo Linha.
        Tempo = TARGET_DATA_PrimeiraOr_Degrau[0, :]
        Degrau = TARGET_DATA_PrimeiraOr_Degrau[1, :]
        Temperatura = TARGET_DATA_PrimeiraOr_Saida[1, :]

    return Tempo, Degrau, Temperatura, file_name

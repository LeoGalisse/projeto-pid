import os
import scipy.io

class ImportarDados:
    def __init__(self):
        pass

    def importar_dados(self):
      # Caminho para o diretório contendo os datasets
      directory = os.path.join(os.getcwd())

      # Listar arquivos .mat no diretório
      files = [f for f in os.listdir(directory) if f.endswith('.mat')]

      # Verificar se há pelo menos um arquivo .mat no diretório
      if len(files) > 0:
          # Listar os arquivos disponíveis para o usuário
          print("Arquivos disponíveis:")
          for i, file in enumerate(files):
              print(f"{i+1}. {file}")

          # Solicitar ao usuário que selecione um arquivo pelo número correspondente
          selected_index = int(input("Selecione o número do arquivo desejado: ")) - 1

          # Verificar se o índice selecionado está dentro dos limites
          if 0 <= selected_index < len(files):
              selected_file = files[selected_index]
              # Carregar o arquivo .mat
              mat_contents = scipy.io.loadmat(os.path.join(directory, selected_file))
              # Extrair os dados
              print("Dataset carregado com sucesso!")
              return mat_contents, selected_file
          else:
              print("Índice inválido. A execução será encerrada.")
              return
      else:
          print("Nenhum arquivo .mat encontrado no diretório. Certifique-se de que os arquivos estão no local correto.")
          return

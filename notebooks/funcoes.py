import requests 
import urllib
import pandas as pd

def importa_salva_dados(url,filename,pasta='../src/data/'):
    resposta = requests.get(url)
    urllib.request.urlretrieve(url,filename=pasta+filename)
    
def le_dados(caminho = '../src/data/adult_names.csv'):
    with open(caminho, 'r') as file: lines = file.read().split('\n')
    # seleciona ultimas linhas e separa pelos :
    lines_ = [line.split(': ') for line in lines[-15:]]
    #faz um loop pelas linhas selecionando o primeiro elemento
    headers = [head[0] for head in lines_[:]]
    # nomeia a coluna com a variável alvo
    headers[-1] = 'target'
    data = pd.read_csv('../src/data/adult_data.csv',header = None, delimiter=(', '))
    data.columns = headers
    return data
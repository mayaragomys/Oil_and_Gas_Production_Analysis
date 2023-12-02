# Imports
import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join

estados_sigla = {
    'Acre': 'AC',
    'Alagoas': 'AL',
    'Amapa': 'AP',
    'Amazonas': 'AM',
    'Bahia': 'BA',
    'Ceará': 'CE',
    'Distrito Federal': 'DF',
    'Espírito Santo': 'ES',
    'Goias': 'GO',
    'Maranhão': 'MA',
    'Mato Grosso': 'MT',
    'Mato Grosso do Sul': 'MS',
    'Minas Gerais': 'MG',
    'Pará': 'PA',
    'Paraná': 'PB',
    'Parana': 'PR',
    'Pernambuco': 'PE',
    'Piaui': 'PI',
    'Rio de Janeiro': 'RJ',
    'Rio Grande do Norte': 'RN',
    'Rio Grande do Sul': 'RS',
    'Rondonia': 'RO',
    'Roraima': 'RR',
    'Santa Catarina': 'SC',
    'SÃO PAULO': 'SP',
    'Sergipe': 'SE',
    'Tocantins': 'TO'
}

def clear_dataset(path, colunas, dropRows=6, dropCols=[]):
    """
    Limpa um conjunto de dados carregado de um arquivo CSV.

    Parâmetros:
    - path (str): Caminho do arquivo CSV.
    - colunas (list): Lista de nomes de colunas, se None, nenhum cabeçalho será usado.
    - dropRows (int): Número de linhas a serem removidas no início do conjunto de dados.
    - dropCols (list): Lista de nomes de colunas a serem removidas.

    Retorna:
    - pandas.DataFrame: Conjunto de dados limpo.
    """
    # 1- Carrega o dataset e Lê o arquivo utilizando as colunas informadas
    if colunas:
        dataset = pd.read_csv(path, names=colunas, skiprows=0, delimiter=';')
    else:
        dataset = pd.read_csv(path, skiprows=0, delimiter=';', header=None)

    # 2- Limpeza dos dados
    # Remove as linhas desnecessárias (n primeiras linhas)
    dataset = dataset.loc[dropRows:]

    # Remove colunas desnecessárias
    if len(dropCols) > 0:
        dataset = dataset.drop(columns=dropCols)

    return dataset


def get_folders(path):
    """
    Retorna uma lista de caminhos para arquivos CSV com o sufixo '_terra.csv' ou '_Terra.csv' em uma pasta.

    Parâmetros:
    - path (str): Caminho da pasta.

    Retorna:
    - list: Lista de caminhos para arquivos CSV correspondentes ao critério especificado.
    """
    # Pegar todos os arquivos dentro da pasta
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    # Filtrar arquivos com sufixo '_terra.csv' ou '_Terra.csv'
    files_terra = [f for f in files if f.lower().endswith('_terra.csv') or f.lower().endswith('_terra.csv')]

    return files_terra
    

def set_ids(dataframe, name_coluna):
    """
    Adiciona uma coluna de IDs ao DataFrame com base nos valores únicos de uma coluna específica.

    Parâmetros:
    - dataframe (pandas.DataFrame): O DataFrame ao qual adicionar a coluna de IDs.
    - name_coluna (str): Nome da coluna para a qual gerar os IDs.

    Modificações:
    - Adiciona uma nova coluna 'ID_' + name_coluna ao DataFrame com IDs associados aos valores únicos da coluna.

    Exemplo:
    set_ids(df, 'nome_coluna')
    """
    # Pega os valores únicos da coluna
    key_mes = dataframe[name_coluna].unique()

    # Gera uma lista de IDs correspondente aos valores únicos
    value_mes = list(range(1, len(key_mes) + 1))

    # Cria um dicionário mapeando valores únicos para IDs
    dict_from_list = {k: v for k, v in zip(key_mes, value_mes)}

    # Adiciona a coluna 'ID_' + name_coluna ao DataFrame com base no mapeamento
    dataframe['ID_' + name_coluna] = dataframe[name_coluna].map(dict_from_list)


def create_folder(path):
    """
    Cria uma nova pasta no caminho especificado, se ela ainda não existir.

    Parâmetros:
    - path (str): Caminho da pasta a ser criada.

    Saída:
    - Imprime uma mensagem indicando se a pasta já existe ou se foi criada com sucesso.
    """
    if os.path.isdir(path): 
        print('A pasta já existe!')
    else:
        os.mkdir(path)
        print('Pasta criada com sucesso!')


def dataframe_region(df, region='Estado'):
    """
    Cria um novo DataFrame agregando a produção de petróleo e gás natural por ano e região.

    Parâmetros:
    - df (pandas.DataFrame): DataFrame contendo os dados originais.
    - region (str): Nome da coluna que representa a região (padrão é 'Estado').

    Retorna:
    - pandas.DataFrame: Novo DataFrame agregado por ano e região com produção de petróleo e gás natural.
    """
    #region=["Estado", "Bacia"]
    # Produção por ano de petróleo de gás
    dataset_estados = df[['Período', region, 'Petróleo (bbl/dia)', 'Gás Natural_total (Mm³/dia)']]
    dataset_estados['Período'] = dataset_estados['Período'].map(lambda x: str(x))

    dataset_estados = dataset_estados.groupby(by=['Período', region]).sum().groupby(level=[0]).cumsum().reset_index()
    dataset_estados['Período'] = pd.to_datetime(dataset_estados['Período']).dt.year
    dataset_estados = dataset_estados.groupby(by=['Período', region]).sum().groupby(level=[0]).cumsum().reset_index()

    dataset_estados['Petróleo (bbl/dia)'] = dataset_estados['Petróleo (bbl/dia)']/12
    dataset_estados['Gás Natural_total (Mm³/dia)'] = dataset_estados['Gás Natural_total (Mm³/dia)']/12

    dataset_estados['Petróleo (bbl/dia)'] = dataset_estados['Petróleo (bbl/dia)'].apply(np.ceil)
    dataset_estados['Gás Natural_total (Mm³/dia)'] = dataset_estados['Gás Natural_total (Mm³/dia)'].apply(np.ceil)

    return dataset_estados


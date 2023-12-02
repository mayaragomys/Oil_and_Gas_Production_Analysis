# Imports
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as ms # para tratamento de missings
from matplotlib import cm
from utils import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json
import plotly.express as px


def subplot_line(df_line):
    """
    Cria um gráfico de linhas com subplots para a evolução da produção de petróleo e gás natural.

    Parâmetros:
    - df_line (pandas.DataFrame): DataFrame contendo os dados a serem plotados.

    Saída:
    - Exibe o gráfico interativo usando a biblioteca Plotly.
    """
    # Create traces
    fig_line = make_subplots(rows=2, cols=1)
    #fig = go.Figure()
    fig_line.add_trace(go.Scatter(x=df_line['Período'].values, y=df_line['Petróleo (bbl/dia)'].values,
                        mode='lines+markers',
                        name='Petróleo (bbl/dia)',
                        text=["Text A", "Text B", "Text C"],
                        textposition="top right",
                        textfont=dict(
                            family="sans serif",
                            size=18,
                            color="crimson"
                        )),
                        row=1, col=1)
    fig_line.add_trace(go.Scatter(x=df_line['Período'].values, y=df_line['Gás Natural_total (Mm³/dia)'].values,
                        mode='lines+markers',
                        name='Gás Natural (Mm³/dia)'),
                        row=2, col=1)

    # Update xaxis properties
    fig_line.update_xaxes(title_text="Ano", row=2, col=1)

    # Edit the layout
    fig_line.update_layout(title='Evolução da produção de petróleo de gás natural')

    fig_line.show()

def subplot_bar(df_line):
    """
    Cria um gráfico de barras com subplots para a evolução da produção de petróleo e gás natural.

    Parâmetros:
    - df_line (pandas.DataFrame): DataFrame contendo os dados a serem plotados.

    Saída:
    - Exibe o gráfico interativo usando a biblioteca Plotly.
    """
    # Create traces
    fig_bar = make_subplots(rows=2, cols=1)
    fig_bar.add_trace(go.Bar(name='Petróleo (bbl/dia)', x=df_line['Período'].values, y=df_line['Petróleo (bbl/dia)'].values), 

                    row=1, col=1)
    fig_bar.add_trace(go.Bar(name='Gás Natural (Mm³/dia)', x=df_line['Período'].values, y=df_line['Gás Natural_total (Mm³/dia)'].values),

                    row=2, col=1)

    # Update xaxis properties
    fig_bar.update_xaxes(title_text="Ano", row=2, col=1)
    # Update yaxis properties
    fig_bar.update_layout(title='Evolução da produção de petróleo de gás natural', margin={"r":0,"l":0,"b":0})
    fig_bar.show()


def subplot_area(df_line):
    """
    Cria um gráfico de área com subplots para a evolução da produção de petróleo e gás natural.

    Parâmetros:
    - df_line (pandas.DataFrame): DataFrame contendo os dados a serem plotados.

    Saída:
    - Exibe o gráfico interativo usando a biblioteca Plotly.
    """

    fig_area = make_subplots(rows=2, cols=1)
    x= df_line['Período'].values

    fig_area.add_trace(go.Scatter(
        x=x, y=df_line['Petróleo (bbl/dia)'].values,
        fill='tozeroy',
        mode='lines',
        name='Petróleo (bbl/dia)',
    ), row=1, col=1)
    fig_area.add_trace(go.Scatter(
        x=x, y=df_line['Gás Natural_total (Mm³/dia)'].values,
        fill='tozeroy',
        mode='lines',
        name='Gás Natural (Mm³/dia)',
    ), row=2, col=1)

    fig_area.update_xaxes(title_text="Ano", row=2, col=1)
    # Update yaxis properties
    fig_area.update_layout(title='Evolução da produção de petróleo de gás natural')

    fig_area.show()


def plot_mult_line(dataset_estados, estados, variavel):
    fig_line_2 = go.Figure()
    for i in range(len(estados)):
        dataset_estado = dataset_estados[dataset_estados["Estado"] == estados[i]]

        fig_line_2.add_trace(go.Scatter(x=dataset_estado['Período'].values, y=dataset_estado[variavel].values,
                            mode='lines+markers',
                            name=estados[i]))

    # Edit the layout
    fig_line_2.update_layout(title='Evolução da produção de ' + variavel,
                    xaxis_title='Ano',
                    yaxis_title=variavel)
    fig_line_2.show()


def choropleth(df_estado_choropleth, variavel):
    """
    Cria um mapa choropleth interativo para a produção por estado ao longo do tempo.

    Parâmetros:
    - df_estado_choropleth (pandas.DataFrame): DataFrame contendo os dados de produção por estado.
    - variavel (str): Nome da variável a ser visualizada no mapa (por exemplo, 'Petróleo (bbl/dia)').

    Saída:
    - Exibe o mapa choropleth usando a biblioteca Plotly Express.
    """
    # Carrega os dados de localização para o mapa
    geojson = json.load(open('brasil_estados.json'))

    fig_choropleth = px.choropleth(df_estado_choropleth, geojson=geojson, locations='Estados',
                                hover_name="Estados", 
                                color=variavel,
                                color_continuous_scale="Reds",
                                scope='south america', animation_frame="Período",
                                )
    fig_choropleth.update_geos(fitbounds="locations", visible=True)
    fig_choropleth.update_layout(
        height=600,
        title_text = 'Produção de ' + variavel + ' por estado',
        margin={"r":0,"l":0,"b":0}
        )
    fig_choropleth.show()

def plot_bar_horizontal(dataset_estados, variavel):
    """
    Cria um gráfico de barras horizontais animado para a produção por estado ao longo do tempo.

    Parâmetros:
    - dataset_estados (pandas.DataFrame): DataFrame contendo os dados de produção por estado.
    - variavel (str): Nome da variável a ser visualizada no gráfico de barras (por exemplo, 'Petróleo (bbl/dia)').

    Saída:
    - Exibe o gráfico de barras horizontais usando a biblioteca Plotly Express.
    """
    fig = px.bar(dataset_estados[['Período', 'Estado', 'Petróleo (bbl/dia)']], y="Estado", x='Petróleo (bbl/dia)', 
             hover_data=['Petróleo (bbl/dia)'], orientation='h', text_auto='.5s', animation_frame="Período")
    fig.update_layout(
            title_text = 'Produção de ' + variavel + ' por estado'
            )
    fig.show()

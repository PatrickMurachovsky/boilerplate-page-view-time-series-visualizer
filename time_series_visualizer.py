# Importação das bibliotecas necessárias
import matplotlib.pyplot as plt   # Para visualizações gráficas
import pandas as pd               # Para manipulação de dados (DataFrame, CSV, etc.)
import seaborn as sns             # Para gráficos estatísticos bonitos
import numpy as np                # Para operações numéricas
from pandas.plotting import register_matplotlib_converters

# Permite que pandas converta automaticamente datas ao usar matplotlib
register_matplotlib_converters()

# Compatibilidade: corrige o erro de depreciação do np.float em versões mais novas do NumPy
if not hasattr(np, 'float'):
    np.float = float

# Carrega o CSV com os dados de visualizações do fórum
# A coluna 'date' é transformada em tipo datetime e usada como índice do DataFrame
df = pd.read_csv(
    'fcc-forum-pageviews.csv',
    parse_dates=['date'],
    index_col='date'
)

# Remove outliers:
# Filtra os dados para manter apenas valores entre o 2.5º percentil e o 97.5º percentil
lower = df['value'].quantile(0.025)
upper = df['value'].quantile(0.975)
df = df[(df['value'] >= lower) & (df['value'] <= upper)]


# -------------------------------
# Função para criar o gráfico de linha
def draw_line_plot():
    # Cria um gráfico de linha com os acessos diários ao fórum
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)  # Linha vermelha fina
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    return fig


# -------------------------------
# Função para criar o gráfico de barras agrupado por ano/mês
def draw_bar_plot():
    # Copia os dados para não alterar o DataFrame original
    df_bar = df.copy()
    
    # Cria colunas auxiliares de ano e mês
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')  # Nome completo do mês (January, February, ...)

    # Define a ordem correta dos meses para manter consistência nos gráficos
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)

    # Agrupa os dados por ano e mês e calcula a média de visualizações
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()

    # Cria uma tabela pivotada com anos nas linhas e meses nas colunas
    df_pivot = df_grouped.pivot(index='year', columns='month', values='value')

    # Plota o gráfico de barras
    ax = df_pivot.plot(kind='bar', figsize=(12, 10))
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')

    # Ajusta o layout para não cortar labels
    fig = ax.get_figure()
    fig.tight_layout()

    # Salva o gráfico em arquivo
    fig.savefig('bar_plot.png')
    return fig


# -------------------------------
# Função para criar gráficos de caixa (boxplots)
def draw_box_plot():
    # Copia os dados para manipulação
    df_box = df.copy()
    df_box.reset_index(inplace=True)  # Move o índice 'date' para coluna normal

    # Extrai ano e mês (abreviado) das datas
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]  # Jan, Feb, ...

    # Define estilo dos gráficos
    sns.set_style('whitegrid')
    
    # Cria figura com 2 subplots lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(20, 6))

    # Boxplot por ano (tendência de longo prazo)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Boxplot por mês (sazonalidade dentro do ano)
    month_order_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=month_order_abbr, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Ajusta layout para melhor espaçamento
    plt.tight_layout()

    # Salva o gráfico em arquivo
    fig.savefig('box_plot.png')
    return fig

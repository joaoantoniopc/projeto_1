import streamlit as st
import plotly.express as px
import pandas as pd

# Carregando os dados
@st.cache_data(ttl=None, persist=None)  # Nova função de cache
def load_data():
    # Carregando dados de um arquivo CSV
    df = pd.read_csv('df.csv')
    return df

df = load_data()

# Título do aplicativo
st.title("Análise de Vendas")

# Verificando se o DataFrame não está vazio ou None
if df is not None and not df.empty:
    # Criando colunas de ano e mês
    df['ano'] = pd.DatetimeIndex(df['dt_venda']).year
    df['mes'] = pd.DatetimeIndex(df['dt_venda']).month_name()

    # Gráfico de barras com os valores de venda por mês e ano
    st.subheader("Valores de venda por mês e ano")
    vendas_mensais = df.groupby(['ano', 'mes'])['vl_preco'].sum().reset_index()
    fig1 = px.bar(vendas_mensais, x='mes', y='vl_preco', color='ano', title='Vendas Mensais ao Longo dos Anos')
    st.plotly_chart(fig1)

    # Gráfico de rosca com os produtos mais vendidos
    st.subheader("Produtos Mais Vendidos")
    produtos_mais_vendidos = df.groupby('no_medicamento')['vl_preco'].sum().reset_index()
    produtos_mais_vendidos = produtos_mais_vendidos.sort_values(by='vl_preco', ascending=False)
    fig2 = px.pie(produtos_mais_vendidos, names='no_medicamento', values='vl_preco', title='Produtos Mais Vendidos', hole=0.3)
    st.plotly_chart(fig2)

    # Widget de seleção para escolher um produto
    produto_selecionado = st.selectbox('Escolha um produto para ver as vendas:', produtos_mais_vendidos['no_medicamento'])

    # Filtrando o DataFrame para mostrar apenas as vendas do produto selecionado
    vendas_produto_selecionado = df[df['no_medicamento'] == produto_selecionado]

    # Mostrando uma tabela com as vendas do produto selecionado
    st.subheader(f"Vendas de {produto_selecionado}")
    st.dataframe(vendas_produto_selecionado)
else:
    st.error("Não foi possível carregar os dados.")

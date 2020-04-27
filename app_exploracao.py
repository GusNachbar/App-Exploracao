import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Explore seus dados')
st.image('https://media.giphy.com/media/4FQMuOKR6zQRO/giphy.gif', width=500)
st.text('Autor : Gustavo Nachbar')
st.write('[LinkedIn](https://www.linkedin.com/in/gustavo-nachbar-33828012b/)')
st.write('[Github](https://github.com/GusNachbar)')
st.subheader('Comece agora! Basta fazer upload do arquivo csv')

file = st.file_uploader('Faça o upload aqui', type='csv')
if file is not None:

    df = pd.read_csv(file)
    st.subheader(f'Seu dataframe possui {df.shape[1]} colunas e {df.shape[0]} linhas')
    n_input = st.number_input('Quantas linhas quer visualizar?', min_value=1, max_value=len(df))
    st.dataframe(df.head(n_input))

    #nome das colunas
    st.subheader('Aqui está o nome de todas as colunas do dataframe!')
    st.markdown(list(df.columns))

    #describe
    st.subheader('Tenha uma descrição detalhada do dataframe')
    check_desc = st.checkbox('Descrição do dataframe')
    if check_desc:
        st.table(df.describe())

    #valores nulos
    check_null = st.checkbox('Ver valores nulos')
    if check_null:
        null = [df[col].isnull().sum() for col in df.columns]
        aux = pd.DataFrame({'data_types': df.dtypes, 'missing_values': null})
        aux['missing_values%'] = aux['missing_values'] / len(df) * 100
        st.table(aux)


    #Multiselect
    st.subheader('Escolha as colunas para aplicar a medida de correlação ')
    n_cols = [valor for valor in df.columns if df[valor].dtypes == np.int64 or df[valor].dtypes == np.float64]
    select_cols = st.multiselect('Escolha aqui:', (n_cols))
    st.dataframe(df[(select_cols)])

    #Radio de corr
    if select_cols is not None:
        radio_op = st.radio('Qual método de correlação deseja aplicar?', ('Método de Pearson', 'Método de Spearman', 'Heatmap'))
        if radio_op == 'Método de Pearson':
            st.table(df[select_cols].corr())
        if radio_op == 'Método de Spearman':
            st.table(df[select_cols].corr(method='spearman'))
        if radio_op == 'Heatmap':
            sns.heatmap(df[select_cols].corr(), annot=True)
            st.pyplot()

    st.subheader('Medidas Estatisticas das Colunas Selecionadas:')
    #botão Média
    button_mean = st.button('Média')
    if button_mean:
        st.table(df[select_cols].mean())

    #botão mediana
    button_median = st.button('Mediana')
    if button_median:
        st.table(df[select_cols].median())

    #botão std
    button_std = st.button('Desvio Padrão')
    if button_std:
        st.table(df[select_cols].std())

    #botão skweness
    button_skw = st.button('Skweness')
    if button_skw:
        st.table(df[select_cols].skew())

    #botão Kurtosis
    button_kurt = st.button('Kurtosis')
    if button_kurt:
        st.table(df[select_cols].kurtosis())

    #gráficos
    st.subheader('Visualização em Gráficos')
    n_cols = [valor for valor in df.columns if df[valor].dtypes == np.int64 or df[valor].dtypes == np.float64]
    plot = ['Boxplot', 'Scatterplot']
    cols_multi = st.multiselect('Selecione as colunas:', (n_cols))
    radio_grf = st.radio('Gráficos:', plot)
    if cols_multi is not None:
        if radio_grf == 'Boxplot' and len(cols_multi) == 2:
            sns.boxplot(x=df[cols_multi[0]], y=df[cols_multi[1]], width=0.7)
            st.pyplot()
        elif radio_grf == 'Scatterplot' and len(cols_multi) == 2:
            sns.scatterplot(x=df[cols_multi[0]], y=df[cols_multi[1]])
            st.pyplot()
    else:
        pass


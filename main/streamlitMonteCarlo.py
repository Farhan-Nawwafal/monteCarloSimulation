import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('https://github.com/Farhan-Nawwafal/monteCarloSimulation/blob/main/data/supplements-sales-data.xlsx')

st.title('Simulasi Monte Carlo : Prediksi Penjualan')

home_page, analysys = st.tabs(['Main Page', 'Analisis'])

with home_page:
    st.header('Tim 4 IF4')

    col1, col2, col3 = st.columns(3)
    col1.image('./img/idinPhoto.jpg')
    col2.image('./img/faishalPhoto.jpg')
    col3.image('./img/farhanPhoto.jpg')

with analysys: 
    st.header('Hasil Prediksi dan Analisis Data menggunakan Monte Carlo')

    st.subheader('Hasil 100 Kali Simulasi Monte Carlo')

    df_periode_2025 = df[df['Date'] >= '2025-01-01']
    df_periode_2025 = df_periode_2025[df_periode_2025['Category']   == 'Vitamin'].reset_index()
    df_periode_2025 = df_periode_2025.drop('index', axis=1)
    
    df_vitamin = df[df['Category'] == 'Vitamin'].reset_index()
    df_vitamin = df_vitamin.drop('index', axis=1)

    units_sold_freq = df_vitamin['Units Sold'].value_counts().sort_index().reset_index()
    units_sold_freq.columns = ['Units Sold', 'Frequency']

    units_sold_freq['Probability'] = units_sold_freq['Frequency'] / units_sold_freq['Frequency'].sum()

    units_sold_freq['Cumulative Probability'] = units_sold_freq['Probability'].cumsum()

    df_simulasi = units_sold_freq

    # Menetukan jumlah simulasi dan memprediksi Units Sold selama 3 bulan ke depan (12 minggu)
    n_simulasi = 100
    minggu = 12
    bil_acak = np.random.rand(n_simulasi, minggu)

    # Membuat fungsi untuk mapping
    def map_to_units_sold(random_number, dataframe):
        return dataframe.loc[dataframe['Cumulative Probability'] >= random_number, 'Units Sold'].iloc[0]
    
    # Melakukan simulasi
    simulasi = np.zeros((n_simulasi, minggu), dtype=int)
    for i in range(n_simulasi):
        for j in range(minggu):
            simulasi[i, j] = map_to_units_sold(bil_acak[i, j],  df_simulasi)
    total_per_simulasi = simulasi.sum(axis=1)
    rata_rata_simulasi = np.mean(total_per_simulasi)

    st.metric("Rata-rata Penjualan", f"{np.mean(total_per_simulasi):.2f} units")
    st.metric("Minimum", f"{np.min(total_per_simulasi)} units")
    st.metric("Maksimum", f"{np.max(total_per_simulasi)} units")

    fig, ax = plt.subplots()
    hist = ax.hist(total_per_simulasi, bins=30, edgecolor='blue')

    ax.set_title(f'Distribusi Total Units Sold selama {minggu/4:.0f} Bulan ke Depan')
    ax.set_xlabel('Total Units Sold')
    ax.set_ylabel('Frekuensi')
    st.pyplot(fig);




    
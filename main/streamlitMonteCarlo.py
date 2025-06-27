import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('supplements-sales-data.xlsx')

st.title('Simulasi Monte Carlo : Prediksi Penjualan Barang Suplement')

home_page, analysys = st.tabs(['Main Page', 'Analisis'])

with home_page:
    st.header('Tim 4 IF4')

    col1, col2, col3 = st.columns(3)
    with col1: 
        col1.image('./img/idinPhoto.jpg')
        st.write('**Idin Naufal Hakim**')
        st.write('10123157')

    with col2: 
        col2.image('./img/faishalPhoto.jpg')
        st.write('**Muhammad Faishal Rahmani**')
        st.write('10123135')

    with col3: 
        col3.image('./img/farhanPhoto.jpg')
        st.write('**Farhan Nawwafal**')
        st.write('10123470')

    st.subheader("📌 Deskripsi Tugas")
    st.markdown("""
    Aplikasi ini dibuat sebagai tugas dari mata kuliah Pemodelan dan Simulasi.  
    Kelompok kami menerapkan metode **Monte Carlo Simulation** untuk memprediksi penjualan produk yang berkategori *Vitamin* selama 3 bulan ke depan berdasarkan data historis.  
    Hasil analisis ditampilkan secara interaktif menggunakan **Streamlit**.
    """)


with analysys: 
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
    
    low = np.percentile(total_per_simulasi, 2.5)
    high = np.percentile(total_per_simulasi, 97.5)
    st.info(f"95% prediksi penjualan akan berada antara {int(low)} dan {int(high)} units.")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rata-rata Penjualan", f"{rata_rata_simulasi:.0f} units")

    col2.metric("Minimum", f"{np.min(total_per_simulasi)} units")
    
    col3.metric("Maksimum", f"{np.max(total_per_simulasi)} units")

    fig, ax = plt.subplots()
    hist = ax.hist(total_per_simulasi, bins=30, edgecolor='blue')

    ax.set_title(f'Distribusi Total Units Sold selama {minggu/4:.0f} Bulan ke Depan')
    ax.set_xlabel('Total Units Sold')
    ax.set_ylabel('Frekuensi')
    st.pyplot(fig);

    st.markdown(f"""
    ### 🔍 Interpretasi Simulasi
    - Rata-rata penjualan selama 3 bulan ke depan diperkirakan: **{rata_rata_simulasi:.0f} units**
    - Ini lebih tinggi dibanding periode Jan–Mar 2025 (**147 units**), yang kemungkinan tercatat sebagian saja.
    - 95% hasil simulasi berada antara **{int(low)} – {int(high)}**.
""")








    
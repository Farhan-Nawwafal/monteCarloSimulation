import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    
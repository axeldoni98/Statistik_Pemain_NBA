import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# membuat judul
st.title("Statistik Pemain NBA")

# membuat markdown
st.markdown("""
Aplikasi Web Scraping dataset Statistik Pemain NBA
""")

# membuat sidebar dari tahun 1950 - 2023
st.sidebar.header("Input Fitur Pengguna")
tahun_dipilih = st.sidebar.selectbox("Tahun",list(reversed(range(1950,2024))))

# web scraping
@st.cache_data
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Umur'].index)
    raw = raw.fillna(0)
    statistik_pemain = raw.drop(['Rk'],axis=1)
    return statistik_pemain
statistik_pemain = load_data(tahun_dipilih)

# sidebar untuk memilih tim
urutan_tim = sorted(statistik_pemain.Tm.unique())
tim_dipilh = st.sidebar.multiselect('Tim',urutan_tim, urutan_tim)

# sidebar untuk posisi
posisi = ['PG','SG','SF','PF','C']
posisi_dipilih = st.sidebar.multiselect('Posisi',posisi, posisi)

# memfilter data
df_tim_dipilih = statistik_pemain[(statistik_pemain.Tm.isin(tim_dipilh)) & (statistik_pemain.Pos.isin(posisi_dipilih))]

st.header("Menampilkan Statistik pemain dari Tim(s)")
st.write('Dimensi Data: ' + str(df_tim_dipilih.shape[0]) + ' Baris dan ' + str(df_tim_dipilih.shape[1]) + ' Kolom.')
st.dataframe(df_tim_dipilih)

# download data statistika pemain NBA
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href
st.markdown(filedownload(df_tim_dipilih),unsafe_allow_html=True)

# membuat Heatmap
# if st.button("Intercorrelation Heatmap"):
    #st.header("intercorrelatuin Matrix Heatmap")
    #df_tim_dipilih.to_csv('output.csv',index=False)
    #df = pd.read_csv('output.csv')

    #corr = df.corr()
   # mask = np.zeros_like(corr)
   # mask[np.tril_indices_from(mask)] = True
   # with sns.axes_style("white"):
   #     f, ax = plt.subplots(figsize=(7,5))
   #     ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
   # st.pyplot()

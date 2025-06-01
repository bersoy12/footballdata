
import scripts.streamlit.streamlit as st
import pandas as pd
from sql_alchemy import fetch_data
from scripts.main import veri_cek
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Futbol Veri Çekme Aracı", layout="wide")

st.title("Futbol Veri Çekme ve Analiz Aracı")

st.sidebar.header("Veri Çekme Ayarları")

tournament_id = st.sidebar.number_input("Turnuva Kodu", value=52, help="Örn: Süper Lig için 52")
country_alpha = st.sidebar.text_input("Ülke Kodu", value='TR', help="Örn: Türkiye için TR")
season_id = st.sidebar.number_input("Sezon Kodu", value=63814, help="2023-2024 sezonu için 63814")
start_week = st.sidebar.number_input("Başlangıç Haftası", value=1, min_value=1, max_value=100)
end_week = st.sidebar.number_input("Bitiş Haftası", value=1, min_value=1, max_value=100)

if st.sidebar.button("Verileri Çek", type="primary"):
    with st.spinner("Veriler çekiliyor..."):
        try:
            veri_cek(
                tournament_id=tournament_id,
                country_alpha=country_alpha,
                season_id=season_id,
                start_week=start_week,
                end_week=end_week
            )
            st.sidebar.success("Veriler başarıyla çekildi!")
        except Exception as e:
            st.sidebar.error(f"Hata oluştu: {str(e)}")


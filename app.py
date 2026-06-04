import streamlit as st
import pandas as pd
from pathlib import Path

from components.style import load_css
from components.sidebar import render_sidebar

from pages_content.overview import render_overview
from pages_content.respondent_profile import render_respondent_profile
from pages_content.usage_competitor import render_usage_competitor

st.set_page_config(
    page_title="Dashboard Survei Bank XYZ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()


@st.cache_data
def load_data():
    file_path = Path("hasil_cleaning_data_dc.xlsx")

    if not file_path.exists():
        st.error(
            "File hasil_cleaning_data_dc.xlsx belum ditemukan di folder yang sama dengan app.py"
        )
        st.stop()

    df = pd.read_excel(file_path, sheet_name="data_clean")

    try:
        attribute_long = pd.read_excel(file_path, sheet_name="attribute_long")
    except Exception:
        attribute_long = pd.DataFrame()

    try:
        codebook = pd.read_excel(file_path, sheet_name="codebook_clean")
    except Exception:
        codebook = pd.DataFrame()

    return df, attribute_long, codebook


df, attribute_long, codebook = load_data()

page, filtered_df, filters = render_sidebar(df)

if page == "Overview":
    render_overview(filtered_df)

elif page == "Profil Responden":
    render_respondent_profile(filtered_df)

elif page == "Usage & Competitor":
    render_usage_competitor(filtered_df)

elif page == "Satisfaction & NPS":
    st.markdown(
        '<div class="page-title">Satisfaction & NPS</div>', unsafe_allow_html=True
    )
    st.info("Page ini belum dibuat.")

elif page == "Layanan Cabang":
    st.markdown('<div class="page-title">Layanan Cabang</div>', unsafe_allow_html=True)
    st.info("Page ini belum dibuat.")

elif page == "Attribute Performance":
    st.markdown(
        '<div class="page-title">Attribute Performance</div>', unsafe_allow_html=True
    )
    st.info("Page ini belum dibuat.")

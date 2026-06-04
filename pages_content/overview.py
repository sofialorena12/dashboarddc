import streamlit as st
import pandas as pd
import plotly.express as px
from components.cards import metric_card


def count_unique(data, col):
    if col in data.columns:
        return data[col].dropna().nunique()
    return 0


def get_mean(data, col):
    if col in data.columns:
        return pd.to_numeric(data[col], errors="coerce").mean()
    return None


def calculate_nps(series):
    series = pd.to_numeric(series, errors="coerce").dropna()

    if len(series) == 0:
        return 0

    promoters = (series >= 9).sum()
    detractors = (series <= 6).sum()

    return round(((promoters / len(series)) - (detractors / len(series))) * 100, 1)


def render_header():
    top_left, top_right = st.columns([6, 2])

    with top_left:
        st.markdown('<div class="page-title">Overview</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="page-subtitle">Gambaran umum performa survei nasabah Bank XYZ</div>',
            unsafe_allow_html=True,
        )

    with top_right:
        st.markdown(
            """
        <div style="display:flex; gap:10px; justify-content:flex-end; margin-top:10px;">
            <div style="background:white; border:1px solid #e5e7eb; border-radius:10px; padding:10px 16px; font-size:14px;">
                📅 1 Apr – 30 Apr 2024
            </div>
            <div style="background:white; border:1px solid #e5e7eb; border-radius:10px; padding:10px 16px; font-size:14px;">
                ⬇ Export
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_kpis(filtered_df):
    total_respondents = len(filtered_df)
    total_prov = count_unique(filtered_df, "PROV")
    total_branch = count_unique(filtered_df, "CABANG")

    avg_sat = get_mean(filtered_df, "E1A_num")
    avg_sat_text = (
        f"{avg_sat:.2f} / 5" if avg_sat is not None and pd.notna(avg_sat) else "-"
    )

    nps_value = (
        calculate_nps(filtered_df["G1A_num"]) if "G1A_num" in filtered_df.columns else 0
    )

    wait_values = []
    for col in ["TL5", "CS5"]:
        if col in filtered_df.columns:
            wait_values.append(pd.to_numeric(filtered_df[col], errors="coerce"))

    if wait_values:
        avg_wait = pd.concat(wait_values).mean()
        avg_wait_text = f"{avg_wait:.1f} menit" if pd.notna(avg_wait) else "-"
    else:
        avg_wait_text = "-"

    k1, k2, k3, k4, k5, k6 = st.columns(6)

    with k1:
        metric_card(
            "Total Responden",
            f"{total_respondents:,}",
            "vs periode sebelumnya",
            "↑ 8.4%",
        )

    with k2:
        metric_card(
            "Total Provinsi", f"{total_prov}", "vs periode sebelumnya", "— 0.0%"
        )

    with k3:
        metric_card(
            "Total Cabang", f"{total_branch}", "vs periode sebelumnya", "↑ 2.6%"
        )

    with k4:
        metric_card(
            "Avg. Satisfaction", avg_sat_text, "vs periode sebelumnya", "↑ 0.08"
        )

    with k5:
        metric_card(
            "NPS Bank XYZ", f"{nps_value}", "vs periode sebelumnya", "↑ 4.3 poin"
        )

    with k6:
        metric_card(
            "Avg. Waktu Tunggu",
            avg_wait_text,
            "vs periode sebelumnya",
            "↓ 0.8 menit",
            "down",
        )


def render_province_chart(filtered_df):
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Distribusi Responden per Provinsi</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="chart-subtitle">Jumlah responden</div>', unsafe_allow_html=True
        )

        if "PROV" not in filtered_df.columns:
            st.info("Kolom PROV tidak ditemukan.")
            return

        prov_data = (
            filtered_df["PROV"]
            .dropna()
            .astype(str)
            .value_counts()
            .head(10)
            .reset_index()
        )
        prov_data.columns = ["Provinsi", "Jumlah Responden"]

        fig = px.bar(
            prov_data,
            x="Provinsi",
            y="Jumlah Responden",
            text="Jumlah Responden",
            color_discrete_sequence=["#14b8a6"],
        )

        max_y = prov_data["Jumlah Responden"].max()

        fig.update_traces(textposition="outside", cliponaxis=False)

        fig.update_layout(
            height=365,
            margin=dict(l=10, r=10, t=55, b=65),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="#0f172a", size=12),
            showlegend=False,
            yaxis=dict(
                title="Jumlah Responden",
                showgrid=False,
                zeroline=False,
                range=[0, max_y * 1.22],
            ),
            xaxis=dict(title="Provinsi", showgrid=False, zeroline=False, tickangle=25),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_branch_chart(filtered_df):
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Top 10 Cabang Berdasarkan Jumlah Responden</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="chart-subtitle">Jumlah responden</div>', unsafe_allow_html=True
        )

        if "CABANG" not in filtered_df.columns:
            st.info("Kolom CABANG tidak ditemukan.")
            return

        branch_data = (
            filtered_df["CABANG"]
            .dropna()
            .astype(str)
            .value_counts()
            .head(10)
            .sort_values(ascending=True)
            .reset_index()
        )
        branch_data.columns = ["Cabang", "Jumlah Responden"]

        fig = px.bar(
            branch_data,
            x="Jumlah Responden",
            y="Cabang",
            orientation="h",
            text="Jumlah Responden",
            color_discrete_sequence=["#08245c"],
        )

        max_x = branch_data["Jumlah Responden"].max()

        fig.update_traces(textposition="outside", cliponaxis=False)

        fig.update_layout(
            height=365,
            margin=dict(l=10, r=55, t=35, b=55),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="#0f172a", size=12),
            showlegend=False,
            xaxis=dict(
                title="Jumlah Responden",
                showgrid=False,
                zeroline=False,
                range=[0, max_x * 1.15],
            ),
            yaxis=dict(title="Cabang", showgrid=False, zeroline=False),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_gender_chart(filtered_df):
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Distribusi Gender</div>', unsafe_allow_html=True
        )

        if "S1" not in filtered_df.columns:
            st.info("Kolom S1 tidak ditemukan.")
            return

        gender_data = (
            filtered_df["S1"].dropna().astype(str).value_counts().reset_index()
        )
        gender_data.columns = ["Gender", "Jumlah"]

        fig = px.pie(
            gender_data,
            names="Gender",
            values="Jumlah",
            hole=0.55,
            color_discrete_sequence=["#08245c", "#14b8a6"],
        )

        fig.update_layout(
            height=315,
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor="white",
            showlegend=True,
            font=dict(color="#0f172a", size=12),
            annotations=[
                dict(
                    text=f"{len(filtered_df):,}<br>Total",
                    x=0.5,
                    y=0.5,
                    font_size=16,
                    showarrow=False,
                )
            ],
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_age_chart(filtered_df):
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Distribusi Usia</div>', unsafe_allow_html=True
        )
        st.markdown(
            '<div class="chart-subtitle">Jumlah responden</div>', unsafe_allow_html=True
        )

        if "S2_2" not in filtered_df.columns:
            st.info("Kolom S2_2 tidak ditemukan.")
            return

        age_data = filtered_df["S2_2"].dropna().astype(str).value_counts().reset_index()
        age_data.columns = ["Kelompok Usia", "Jumlah Responden"]

        fig = px.bar(
            age_data,
            x="Kelompok Usia",
            y="Jumlah Responden",
            text="Jumlah Responden",
            color_discrete_sequence=["#14b8a6"],
        )

        max_y = age_data["Jumlah Responden"].max()

        fig.update_traces(textposition="outside", cliponaxis=False)

        fig.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=55, b=65),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="#0f172a", size=12),
            showlegend=False,
            yaxis=dict(
                title="Jumlah Responden",
                showgrid=False,
                zeroline=False,
                range=[0, max_y * 1.22],
            ),
            xaxis=dict(
                title="Kelompok Usia", showgrid=False, zeroline=False, tickangle=25
            ),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_key_insights():
    st.markdown(
        """
    <div class="insight-box">
        <div class="insight-title">💡 Key Insights</div>
        <ul>
            <li>Grafik provinsi menunjukkan wilayah dengan jumlah responden paling dominan.</li>
            <li>Cabang dengan responden terbanyak dapat menjadi prioritas awal untuk evaluasi layanan.</li>
            <li>Distribusi gender dan usia membantu memahami karakteristik utama responden.</li>
            <li>Avg. Satisfaction dan NPS digunakan sebagai indikator utama pengalaman nasabah.</li>
            <li>Avg. waktu tunggu menunjukkan efisiensi layanan cabang, khususnya teller dan customer service.</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_overview(filtered_df):
    render_header()
    render_kpis(filtered_df)

    # Jarak antara KPI dan chart utama
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    row1_col1, row1_col2 = st.columns([1.1, 1.45])

    with row1_col1:
        render_province_chart(filtered_df)

    with row1_col2:
        render_branch_chart(filtered_df)

    # Jarak antara row chart atas dan row chart bawah
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    row2_col1, row2_col2, row2_col3 = st.columns([0.8, 1.25, 1.4])

    with row2_col1:
        render_gender_chart(filtered_df)

    with row2_col2:
        render_age_chart(filtered_df)

    with row2_col3:
        render_key_insights()

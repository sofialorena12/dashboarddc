import streamlit as st
import pandas as pd
import plotly.express as px
from components.cards import metric_card


# =====================================================
# Helper
# =====================================================
def safe_numeric(series):
    return pd.to_numeric(series, errors="coerce")


def count_unique(data, col):
    if col in data.columns:
        return data[col].dropna().nunique()
    return 0


def get_percentage(data, col, target_keywords):
    """
    Menghitung persentase berdasarkan kata kunci tertentu.
    Contoh: target_keywords = ["wanita", "perempuan"]
    """
    if col not in data.columns or len(data) == 0:
        return 0

    series = data[col].dropna().astype(str).str.lower()

    if len(series) == 0:
        return 0

    mask = series.apply(lambda x: any(keyword in x for keyword in target_keywords))

    return round((mask.sum() / len(series)) * 100, 1)


def make_value_counts(data, col, name_col, value_col, top_n=None, ascending=False):
    if col not in data.columns:
        return pd.DataFrame(columns=[name_col, value_col])

    result = data[col].dropna().astype(str).value_counts()

    if top_n:
        result = result.head(top_n)

    if ascending:
        result = result.sort_values(ascending=True)

    result = result.reset_index()
    result.columns = [name_col, value_col]

    return result


def clean_tenure_label(value):
    value = str(value)

    mapping = {
        "1 bulan s/d 3 bulan": "1–3 bulan",
        "3 bulan s/d 11 bulan": "3–11 bulan",
        "1 tahun s/d 2 tahun 11 bulan": "1–2 tahun",
        "3 tahun s/d 4 tahun 11 bulan": "3–4 tahun",
        "5 tahun atau lebih": "≥ 5 tahun",
    }

    return mapping.get(value, value)


def clean_frequency_label(value):
    value = str(value)

    mapping = {
        "Setiap hari": "Harian",
        "Beberapa kali dalam seminggu": "Mingguan",
        "Beberapa kali dalam sebulan": "Bulanan",
        "Jarang": "Jarang",
    }

    return mapping.get(value, value)


def apply_chart_layout(fig, height=330, margin_top=45, margin_bottom=55):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=20, t=margin_top, b=margin_bottom),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#0f172a", size=12),
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    )

    return fig


# =====================================================
# Header
# =====================================================
def render_header():
    top_left, top_right = st.columns([6, 2])

    with top_left:
        st.markdown(
            '<div class="page-title">Profil Responden</div>', unsafe_allow_html=True
        )
        st.markdown(
            '<div class="page-subtitle">Gambaran karakteristik demografis dan profil nasabah</div>',
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


# =====================================================
# KPI
# =====================================================
def render_kpis(filtered_df):
    total_respondents = len(filtered_df)

    if "S2_1" in filtered_df.columns:
        avg_age = safe_numeric(filtered_df["S2_1"]).mean()
        avg_age_text = f"{avg_age:.1f}" if pd.notna(avg_age) else "-"
    else:
        avg_age_text = "-"

    female_pct = get_percentage(filtered_df, "S1", ["wanita", "perempuan", "female"])
    female_text = f"{female_pct:.1f}%"

    existing_pct = get_percentage(filtered_df, "S3", ["ya", "nasabah", "existing"])
    existing_text = f"{existing_pct:.1f}%"

    # Frequent transactor dihitung dari responden yang frekuensi transaksinya bukan kosong.
    # Kalau kategori S7 berbeda, nanti bisa disesuaikan lagi.
    if "S7" in filtered_df.columns and len(filtered_df) > 0:
        freq_series = filtered_df["S7"].dropna().astype(str)
        frequent_pct = round((len(freq_series) / len(filtered_df)) * 100, 1)
    else:
        frequent_pct = 0

    frequent_text = f"{frequent_pct:.1f}%"

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        metric_card(
            "Total Responden",
            f"{total_respondents:,}",
            "vs periode sebelumnya",
            "↑ 8.4%",
        )

    with k2:
        metric_card("Avg. Usia", avg_age_text, "berdasarkan data usia", "↑ 0.9 tahun")

    with k3:
        metric_card("Wanita", female_text, "berdasarkan gender", "↑ 2.0 poin")

    with k4:
        metric_card(
            "Existing Customer",
            existing_text,
            "berdasarkan status nasabah",
            "↑ 1.6 poin",
        )

    with k5:
        metric_card(
            "Aktif Bertransaksi",
            frequent_text,
            "berdasarkan frekuensi transaksi",
            "↑ 2.3 poin",
        )


# =====================================================
# Charts
# =====================================================
def render_age_distribution(filtered_df):
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

        age_data = make_value_counts(
            filtered_df, "S2_2", "Kelompok Usia", "Jumlah Responden"
        )

        if age_data.empty:
            st.info("Data usia tidak tersedia.")
            return

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
            height=335,
            margin=dict(l=10, r=10, t=55, b=65),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="#0f172a", size=12),
            showlegend=False,
            yaxis=dict(
                title="Jumlah Responden",
                showgrid=False,
                zeroline=False,
                range=[0, max_y * 1.25],
            ),
            xaxis=dict(
                title="Kelompok Usia", showgrid=False, zeroline=False, tickangle=25
            ),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_gender_distribution(filtered_df):
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Distribusi Gender</div>', unsafe_allow_html=True
        )

        if "S1" not in filtered_df.columns:
            st.info("Kolom S1 tidak ditemukan.")
            return

        gender_data = make_value_counts(filtered_df, "S1", "Gender", "Jumlah")

        if gender_data.empty:
            st.info("Data gender tidak tersedia.")
            return

        fig = px.pie(
            gender_data,
            names="Gender",
            values="Jumlah",
            hole=0.55,
            color_discrete_sequence=["#08245c", "#14b8a6"],
        )

        fig.update_layout(
            height=335,
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


def render_customer_tenure(filtered_df):
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Lama Menjadi Nasabah</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="chart-subtitle">Jumlah responden</div>', unsafe_allow_html=True
        )

        if "S4" not in filtered_df.columns:
            st.info("Kolom S4 tidak ditemukan.")
            return

        tenure_data = make_value_counts(
            filtered_df,
            "S4",
            "Lama Menjadi Nasabah",
            "Jumlah Responden",
            ascending=True,
        )

        if tenure_data.empty:
            st.info("Data lama menjadi nasabah tidak tersedia.")
            return

        tenure_data["Label"] = tenure_data["Lama Menjadi Nasabah"].apply(
            clean_tenure_label
        )

        fig = px.bar(
            tenure_data,
            x="Jumlah Responden",
            y="Label",
            orientation="h",
            text="Jumlah Responden",
            color_discrete_sequence=["#08245c"],
        )

        max_x = tenure_data["Jumlah Responden"].max()

        fig.update_traces(textposition="outside", cliponaxis=False)

        fig.update_layout(
            height=335,
            margin=dict(l=10, r=55, t=35, b=45),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="#0f172a", size=12),
            showlegend=False,
            xaxis=dict(
                title="Jumlah Responden",
                showgrid=False,
                zeroline=False,
                range=[0, max_x * 1.18],
            ),
            yaxis=dict(title="", showgrid=False, zeroline=False),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_transaction_frequency(filtered_df):
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Frekuensi Transaksi</div>', unsafe_allow_html=True
        )
        st.markdown(
            '<div class="chart-subtitle">Jumlah responden</div>', unsafe_allow_html=True
        )

        if "S7" not in filtered_df.columns:
            st.info("Kolom S7 tidak ditemukan.")
            return

        freq_data = make_value_counts(
            filtered_df, "S7", "Frekuensi Transaksi", "Jumlah Responden"
        )

        if freq_data.empty:
            st.info("Data frekuensi transaksi tidak tersedia.")
            return

        freq_data["Label"] = freq_data["Frekuensi Transaksi"].apply(
            clean_frequency_label
        )

        fig = px.bar(
            freq_data,
            x="Label",
            y="Jumlah Responden",
            text="Jumlah Responden",
            color_discrete_sequence=["#14b8a6"],
        )

        max_y = freq_data["Jumlah Responden"].max()

        fig.update_traces(textposition="outside", cliponaxis=False)

        fig.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=55, b=65),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="#0f172a", size=12),
            showlegend=False,
            yaxis=dict(
                title="Jumlah Responden",
                showgrid=False,
                zeroline=False,
                range=[0, max_y * 1.25],
            ),
            xaxis=dict(
                title="Frekuensi Transaksi",
                showgrid=False,
                zeroline=False,
                tickangle=20,
            ),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_education_level(filtered_df):
    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Pendidikan Terakhir</div>', unsafe_allow_html=True
        )
        st.markdown(
            '<div class="chart-subtitle">Jumlah responden</div>', unsafe_allow_html=True
        )

        if "P3" not in filtered_df.columns:
            st.info("Kolom P3 tidak ditemukan.")
            return

        edu_data = make_value_counts(
            filtered_df, "P3", "Pendidikan", "Jumlah Responden", ascending=True
        )

        if edu_data.empty:
            st.info("Data pendidikan tidak tersedia.")
            return

        fig = px.bar(
            edu_data,
            x="Jumlah Responden",
            y="Pendidikan",
            orientation="h",
            text="Jumlah Responden",
            color_discrete_sequence=["#14b8a6"],
        )

        max_x = edu_data["Jumlah Responden"].max()

        fig.update_traces(textposition="outside", cliponaxis=False)

        fig.update_layout(
            height=320,
            margin=dict(l=10, r=55, t=35, b=45),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="#0f172a", size=12),
            showlegend=False,
            xaxis=dict(
                title="Jumlah Responden",
                showgrid=False,
                zeroline=False,
                range=[0, max_x * 1.18],
            ),
            yaxis=dict(title="", showgrid=False, zeroline=False),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_occupation(filtered_df):
    with st.container(border=True):
        st.markdown('<div class="chart-title">Pekerjaan</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="chart-subtitle">Jumlah responden</div>', unsafe_allow_html=True
        )

        if "P4" not in filtered_df.columns:
            st.info("Kolom P4 tidak ditemukan.")
            return

        occ_data = make_value_counts(
            filtered_df, "P4", "Pekerjaan", "Jumlah Responden", top_n=8, ascending=True
        )

        if occ_data.empty:
            st.info("Data pekerjaan tidak tersedia.")
            return

        fig = px.bar(
            occ_data,
            x="Jumlah Responden",
            y="Pekerjaan",
            orientation="h",
            text="Jumlah Responden",
            color_discrete_sequence=["#14b8a6"],
        )

        max_x = occ_data["Jumlah Responden"].max()

        fig.update_traces(textposition="outside", cliponaxis=False)

        fig.update_layout(
            height=320,
            margin=dict(l=10, r=55, t=35, b=45),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="#0f172a", size=12),
            showlegend=False,
            xaxis=dict(
                title="Jumlah Responden",
                showgrid=False,
                zeroline=False,
                range=[0, max_x * 1.18],
            ),
            yaxis=dict(title="", showgrid=False, zeroline=False),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_key_insights(filtered_df):
    total = len(filtered_df)

    if "S2_2" in filtered_df.columns and total > 0:
        top_age = filtered_df["S2_2"].dropna().astype(str).value_counts().idxmax()
    else:
        top_age = "-"

    if "S1" in filtered_df.columns and total > 0:
        top_gender = filtered_df["S1"].dropna().astype(str).value_counts().idxmax()
    else:
        top_gender = "-"

    if "S4" in filtered_df.columns and total > 0:
        top_tenure = filtered_df["S4"].dropna().astype(str).value_counts().idxmax()
        top_tenure = clean_tenure_label(top_tenure)
    else:
        top_tenure = "-"

    st.markdown(
        f"""
    <div class="insight-box">
        <div class="insight-title">💡 Key Insights</div>
        <ul>
            <li>Kelompok usia paling dominan adalah <b>{top_age}</b>.</li>
            <li>Gender dengan jumlah responden terbanyak adalah <b>{top_gender}</b>.</li>
            <li>Mayoritas responden telah menjadi nasabah selama <b>{top_tenure}</b>.</li>
            <li>Profil responden dapat digunakan untuk memahami segmen nasabah utama Bank XYZ.</li>
            <li>Distribusi pendidikan dan pekerjaan membantu membaca karakteristik sosial ekonomi responden.</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )


# =====================================================
# Main render
# =====================================================
def render_respondent_profile(filtered_df):
    render_header()
    render_kpis(filtered_df)

    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    row1_col1, row1_col2, row1_col3 = st.columns([1.2, 0.9, 1.2])

    with row1_col1:
        render_age_distribution(filtered_df)

    with row1_col2:
        render_gender_distribution(filtered_df)

    with row1_col3:
        render_customer_tenure(filtered_df)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    row2_col1, row2_col2, row2_col3, row2_col4 = st.columns([1.0, 1.15, 1.15, 1.45])

    with row2_col1:
        render_transaction_frequency(filtered_df)

    with row2_col2:
        render_education_level(filtered_df)

    with row2_col3:
        render_occupation(filtered_df)

    with row2_col4:
        render_key_insights(filtered_df)

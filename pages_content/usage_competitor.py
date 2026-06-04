import streamlit as st
import pandas as pd
import plotly.express as px

from components.cards import metric_card


# =====================================================
# HELPER
# =====================================================

def explode_column(df, col):

    temp = (
        df[[col]]
        .dropna()
        .assign(
            split=lambda x: x[col].astype(str).str.split(";")
        )
        .explode("split")
    )

    temp["split"] = temp["split"].str.strip()

    return temp


# =====================================================
# PAGE HEADER
# =====================================================

def render_header():

    st.markdown(
        """
        <div class="page-title">
        Penggunaan & Kompetitor
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="page-subtitle">
        Analisis perilaku penggunaan bank dan lanskap kompetitor
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# KPI CARDS
# =====================================================

def render_kpis(df):

    total_resp = len(df)

    xyz_users = (
        df["A1A"]
        .astype(str)
        .str.contains("Bank XYZ", na=False)
        .sum()
    )

    xyz_usage_pct = (
        xyz_users / total_resp * 100
    )

    saving_pct = (
        (df["A1B"] == "Bank XYZ").sum()
        / total_resp
        * 100
    )

    transaction_pct = (
        (df["A1C"] == "Bank XYZ").sum()
        / total_resp
        * 100
    )

    multi_bank_pct = (
        df["A1A"]
        .astype(str)
        .str.contains(";")
        .mean()
        * 100
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    
    with c1:
        metric_card(
            "Jumlah Responden",
            f"{total_resp:,}",
            sub_text=""
        )

    with c2:
        metric_card(
            "Pengguna Bank XYZ",
            f"{xyz_usage_pct:.1f}%",
            sub_text=""
        )

    with c3:
        metric_card(
            "Bank Utama Menabung",
            f"{saving_pct:.1f}%",
            sub_text=""
        )

    with c4:
        metric_card(
            "Bank Utama Transaksi",
            f"{transaction_pct:.1f}%",
            sub_text=""
        )

    with c5:
        metric_card(
            "Nasabah Multi-Bank (>1 Bank)",
            f"{multi_bank_pct:.1f}%",
            sub_text=""
        )


# =====================================================
# MOST USED BANK / Bank yang Paling Sering Digunakan
# =====================================================

def render_used_bank_chart(df):

    temp = explode_column(df, "A1A")

    bank_count = (
        temp["split"]
        .value_counts()
        .head(10)
        .sort_values()
        .reset_index()
    )

    bank_count.columns = [
        "Bank",
        "Jumlah"
    ]

    bank_count["Persentase"] = (
        bank_count["Jumlah"]
        / len(df)
        * 100
    ).round(1)

    bank_count["Label"] = (
        bank_count["Jumlah"].astype(str)
        + " ("
        + bank_count["Persentase"].astype(str)
        + "%)"
    )

    fig = px.bar(
        bank_count,
        x="Jumlah",
        y="Bank",
        orientation="h",
        text="Label"
    )

    fig.update_layout(
        height=400
    )
    


    with st.container(border=True):

        st.markdown(
            '<div class="chart-title">Bank yang Paling Sering Digunakan</div>',
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =====================================================
# TOP COMPETITOR / Kompetitor Utama
# =====================================================

def render_competitor_chart(df):

    comp = (
        df["KOMP"]
        .dropna()
        .value_counts()
        .head(10)
        .sort_values()
        .reset_index()
    )

    comp.columns = [
        "Bank",
        "Jumlah"
    ]

    comp["Persentase"] = (
        comp["Jumlah"]
        / len(df)
        * 100
    ).round(1)

    comp["Label"] = (
        comp["Jumlah"].astype(str)
        + " ("
        + comp["Persentase"].astype(str)
        + "%)"
    )

    fig = px.bar(
        comp,
        x="Jumlah",
        y="Bank",
        orientation="h",
        text="Label"
    )

    fig.update_layout(
        height=400
    )

    with st.container(border=True):

        st.markdown(
            '<div class="chart-title">Kompetitor Utama</div>',
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =====================================================
# SAVINGS VS TRANSACTION / Perbandingan Bank Utama untuk Menabung dan Transaksi
# =====================================================

def render_savings_transaction(df):

    saving = (
        df["A1B"]
        .value_counts(normalize=True)
        .mul(100)
        .rename("Menabung (%)")
    )

    transaction = (
        df["A1C"]
        .value_counts(normalize=True)
        .mul(100)
        .rename("Transaksi (%)")
    )

    compare = pd.concat(
        [saving, transaction],
        axis=1
    ).fillna(0)

    compare["total"] = (
        compare["Menabung (%)"]
        + compare["Transaksi (%)"]
    )

    compare = (
        compare
        .sort_values("total", ascending=False)
        .head(10)
        .drop(columns="total")
    )

    compare = compare.reset_index()
    compare.rename(columns={"index": "Bank"}, inplace=True)

    st.markdown(
        '<div class="chart-title">Perbandingan Bank Utama untuk Menabung dan Transaksi</div>',
        unsafe_allow_html=True
    )

    fig = px.bar(
        compare,
        x="Bank",
        y=["Menabung (%)", "Transaksi (%)"],
        barmode="group"
    )

    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        legend_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# REASONS FOR TRANSACTION / Alasan Memilih Bank untuk Transaksi
# =====================================================
def shorten_reason(text):

    mapping = {
        "Kemudahan dalam bertransaksi dengan bank lain":
            "Mudah Transfer Antar Bank",

        "Bank digunakan oleh banyak orang":
            "Banyak Digunakan",

        "Memberikan kecepatan dalam transaksi":
            "Transaksi Cepat",

        "Memiliki banyak ATM":
            "Banyak ATM",

        "Memiliki banyak cabang":
            "Banyak Cabang",

        "Fitur transaksi di ATM lengkap":
            "Fitur ATM Lengkap",

        "Memiliki banyak pilihan channel untuk melakukan transaksi (sms banking, internet banking, mobile banking, dll)":
            "Banyak Channel Transaksi",

        "Fitur transaksi di e-channel lengkap":
            "Fitur E-Channel Lengkap",

        "Didukung oleh layanan e-channel/e-banking yang baik":
            "E-Banking Baik",

        "Memberikan keuntungan saat digunakan untuk bertransaksi (diskon, cashback, point rewards)":
            "Promo & Cashback"
    }

    return mapping.get(text, text[:40])

def render_reason_transaction(df):

    data = explode_column(df, "B3")

    data = (
        data["split"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    data.columns = ["Alasan", "Jumlah"]

    data["Alasan"] = data["Alasan"].apply(shorten_reason)
    
    data["Persentase"] = (
        data["Jumlah"]
        / len(df)
        * 100
    ).round(1)

    data["Label"] = (
        data["Jumlah"].astype(str)
        + " ("
        + data["Persentase"].astype(str)
        + "%)"
    )

    st.markdown(
        '<div class="chart-title">Alasan Memilih Bank untuk Transaksi</div>',
        unsafe_allow_html=True
    )

    fig = px.bar(
        data.sort_values("Jumlah"),
        x="Jumlah",
        y="Alasan",
        orientation="h",
        text="Label"
    )

    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    fig.update_traces(
    textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# REASONS FOR SAVING / Alasan Memilih Bank untuk Menabung
# =====================================================

def render_reason_saving(df):

    data = explode_column(df, "B4")

    data = (
        data["split"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    data.columns = ["Alasan", "Jumlah"]
    
    data["Persentase"] = (
        data["Jumlah"]
        / len(df)
        * 100
    ).round(1)

    data["Label"] = (
        data["Jumlah"].astype(str)
        + " ("
        + data["Persentase"].astype(str)
        + "%)"
    )

    data["Alasan"] = data["Alasan"].replace({
        "Aman menabung di bank tersebut/keamanannya terjamin":
            "Aman & Terjamin",

        "Bank tersebut memiliki reputasi yang baik":
            "Reputasi Baik",

        "Biaya administrasi bulanannya rendah":
            "Biaya Admin Rendah",

        "Memiliki banyak produk tabungan untuk kebutuhan yang berbeda":
            "Produk Tabungan Lengkap",

        "Menawarkan suku bunga yang kompetitif":
            "Bunga Kompetitif",

        "Batas saldo mengendap minimalnya rendah":
            "Saldo Minimum Rendah",

        "Banyak melakukan promosi produk tabungan dengan memberikan hadiah langsung (saat pembukaan awal rekening, berdasarkan rata-rata saldo mengendap)":
            "Hadiah Langsung",

        "Banyak melakukan promosi dengan undian berhadiah":
            "Undian Berhadiah",

        "Banyak memberikan promo-promo berhadiah (cashback, point reward, dsb)":
            "Promo Cashback",

        "Tanpa biaya admin bulanan":
            "Tanpa Biaya Admin"
    })

    st.markdown(
        '<div class="chart-title">Alasan Memilih Bank untuk Menabung</div>',
        unsafe_allow_html=True
    )

    fig = px.bar(
        data.sort_values("Jumlah"),
        x="Jumlah",
        y="Alasan",
        orientation="h",
        text="Label"
    )

    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    fig.update_traces(
    textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# ACCOUNT OPENING PURPOSE / Tujuan Membuka Rekening
# =====================================================

def render_account_purpose_tiles(df):

    temp = explode_column(df, "A2")

    purpose = (
        temp["split"]
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
        .head(6)
    )

    purpose.index = purpose.index.map({
        "Untuk menabung":
            "Menabung",

        "Untuk menerima gaji dari tempat saya bekerja":
            "Menerima Gaji",

        "Untuk melakukan transaksi finansial saya sehari-hari (seperti pembayaran tagihan listrik, telepon, pembelian pulsa telepon, pembelian token listrik, dll)":
            "Transaksi Harian",

        "Untuk menunjang bisnis saya (menerima transfer dana dari klien/konsumen saya)":
            "Kebutuhan Bisnis",

        "Sebagai syarat ketika mengambil kredit":
            "Syarat Kredit",

        "Lainnya":
            "Lainnya"
    })

    with st.container(border=True):

        st.markdown(
            '<div class="chart-title">Tujuan Membuka Rekening</div>',
            unsafe_allow_html=True
        )

        cols = st.columns(3)

        for i, (label, pct) in enumerate(purpose.items()):

            with cols[i % 3]:

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-title">{label}</div>
                        <div class="metric-value">{pct:.1f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =====================================================
# KEY INSIGHTS
# =====================================================

def render_insight(df):

    xyz_pct = (
        df["A1A"]
        .astype(str)
        .str.contains("Bank XYZ")
        .mean() * 100
    )

    top_comp = (
        df["KOMP"]
        .value_counts(normalize=True)
        .mul(100)
        .reset_index()
    )

    top_comp_bank = top_comp.iloc[0, 0]
    top_comp_pct = top_comp.iloc[0, 1]

    saving_pct = (
        (df["A1B"] == "Bank XYZ")
        .mean() * 100
    )

    transaction_pct = (
        (df["A1C"] == "Bank XYZ")
        .mean() * 100
    )

    alasan_transaksi = (
        explode_column(df, "B3")["split"]
        .value_counts()
        .index[0]
    )

    alasan_tabungan = (
        explode_column(df, "B4")["split"]
        .value_counts()
        .index[0]
    )

    st.markdown(
        f"""
        <div class="insight-box">

        <div class="insight-title">
        💡 Key Insights
        </div>

        <ul>
        <li>Hampir seluruh responden ({xyz_pct:.1f}%) menggunakan Bank XYZ, menunjukkan penetrasi merek yang sangat kuat.</li>

        <li>{top_comp_bank} merupakan kompetitor utama yang paling sering disebut responden ({top_comp_pct:.1f}%).</li>

        <li>Mayoritas pengguna menjadikan Bank XYZ sebagai bank utama menabung ({saving_pct:.1f}%) maupun transaksi ({transaction_pct:.1f}%).</li>

        <li>{alasan_transaksi} menjadi faktor utama pemilihan bank untuk transaksi.</li>

        <li>{alasan_tabungan} menjadi faktor dominan dalam pemilihan bank untuk menabung.</li>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# MAIN PAGE
# =====================================================

def render_usage_competitor(df):

    render_header()

    render_kpis(df)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        render_used_bank_chart(df)

    with col2:
        render_competitor_chart(df)

    st.markdown("<br>", unsafe_allow_html=True)

    render_savings_transaction(df)

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        render_reason_transaction(df)

    with col4:
        render_reason_saving(df)

    st.markdown("<br>", unsafe_allow_html=True)

    col5, col6 = st.columns([1.5, 1])

    with col5:
        render_account_purpose_tiles(df)

    with col6:
        render_insight(df)
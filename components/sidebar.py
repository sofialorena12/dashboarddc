import streamlit as st


def sidebar_multiselect(label, col, df, label_map=None, custom_order=None):
    if col not in df.columns:
        return []

    options = df[col].dropna().astype(str).unique().tolist()

    if custom_order:
        order_dict = {value: i for i, value in enumerate(custom_order)}
        options = sorted(options, key=lambda x: order_dict.get(x, 999))
    else:
        options = sorted(options)

    def format_label(value):
        if label_map and value in label_map:
            return label_map[value]
        return value

    selected = st.multiselect(
        label,
        options=options,
        default=[],
        placeholder="All",
        format_func=format_label,
    )

    return selected


def apply_filters(df, filters):
    filtered_df = df.copy()

    for col, selected_values in filters.items():
        if col in filtered_df.columns and selected_values:
            filtered_df = filtered_df[
                filtered_df[col].astype(str).isin(selected_values)
            ]

    return filtered_df


def render_sidebar(df):
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-title">
                Dashboard Survei<br>Bank XYZ
            </div>
            """,
            unsafe_allow_html=True,
        )

        # =========================
        # Navigation clickable
        # =========================
        page_label = st.radio(
            "Navigation",
            [
                "▦  Overview",
                "♙  Profil Responden",
                "▮  Usage & Competitor",
                "☻  Satisfaction & NPS",
                "▥  Layanan Cabang",
                "☆  Attribute Performance",
            ],
            label_visibility="collapsed",
        )

        page_mapping = {
            "▦  Overview": "Overview",
            "♙  Profil Responden": "Profil Responden",
            "▮  Usage & Competitor": "Usage & Competitor",
            "☻  Satisfaction & NPS": "Satisfaction & NPS",
            "▥  Layanan Cabang": "Layanan Cabang",
            "☆  Attribute Performance": "Attribute Performance",
        }

        page = page_mapping[page_label]

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Filter")

        # =========================
        # Label ringkas filter
        # =========================
        tenure_label_map = {
            "1 bulan s/d 3 bulan": "1–3 bulan",
            "3 bulan s/d 11 bulan": "3–11 bulan",
            "1 tahun s/d 2 tahun 11 bulan": "1–2 tahun",
            "3 tahun s/d 4 tahun 11 bulan": "3–4 tahun",
            "5 tahun atau lebih": "≥ 5 tahun",
        }

        tenure_order = [
            "1 bulan s/d 3 bulan",
            "3 bulan s/d 11 bulan",
            "1 tahun s/d 2 tahun 11 bulan",
            "3 tahun s/d 4 tahun 11 bulan",
            "5 tahun atau lebih",
        ]

        frequency_label_map = {
            "Setiap hari": "Harian",
            "Beberapa kali dalam seminggu": "Mingguan",
            "Beberapa kali dalam sebulan": "Bulanan",
            "Jarang": "Jarang",
        }

        frequency_order = [
            "Setiap hari",
            "Beberapa kali dalam seminggu",
            "Beberapa kali dalam sebulan",
            "Jarang",
        ]

        # =========================
        # Filter utama
        # =========================
        selected_prov = sidebar_multiselect(
            "Provinsi",
            "PROV",
            df,
        )

        selected_city = sidebar_multiselect(
            "Kabupaten/Kota",
            "KABKOTA",
            df,
        )

        selected_branch = sidebar_multiselect(
            "Cabang",
            "CABANG",
            df,
        )

        selected_gender = sidebar_multiselect(
            "Gender",
            "S1",
            df,
        )

        selected_age = sidebar_multiselect(
            "Kelompok Usia",
            "S2_2",
            df,
        )

        selected_tenure = sidebar_multiselect(
            "Lama Menjadi Nasabah",
            "S4",
            df,
            label_map=tenure_label_map,
            custom_order=tenure_order,
        )

        selected_freq = sidebar_multiselect(
            "Frekuensi Transaksi",
            "S7",
            df,
            label_map=frequency_label_map,
            custom_order=frequency_order,
        )

        selected_comp = sidebar_multiselect(
            "Competitor",
            "KOMP",
            df,
        )

        st.markdown(
            """
            <div class="sidebar-info">
                <b>Periode Survei</b><br>
                1 Apr – 30 Apr 2024
                <hr>
                <b>Data diperbarui</b><br>
                6 Mei 2024 09.30
            </div>
            """,
            unsafe_allow_html=True,
        )

    filters = {
        "PROV": selected_prov,
        "KABKOTA": selected_city,
        "CABANG": selected_branch,
        "S1": selected_gender,
        "S2_2": selected_age,
        "S4": selected_tenure,
        "S7": selected_freq,
        "KOMP": selected_comp,
    }

    filtered_df = apply_filters(df, filters)

    return page, filtered_df, filters

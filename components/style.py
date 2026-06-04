import streamlit as st


def load_css():
    st.markdown(
        """
    <style>
    /* =====================================================
       GLOBAL APP STYLE
    ===================================================== */
    .stApp {
        background-color: #f8fafc;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-left: 1.4rem;
        padding-right: 1.4rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.8rem;
    }

    hr {
        border: none;
        border-top: 1px solid #1e3a5f;
        margin: 22px 0;
    }


    /* =====================================================
       SIDEBAR BACKGROUND
    ===================================================== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #061b3a 0%, #08244d 100%);
        width: 285px !important;
        min-width: 285px !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.4rem;
        padding-left: 1.1rem;
        padding-right: 1.1rem;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    .sidebar-title {
        font-size: 25px;
        font-weight: 900;
        line-height: 1.22;
        margin-bottom: 28px;
        color: #ffffff;
        letter-spacing: 0.2px;
    }

    .sidebar-info {
        font-size: 13px;
        color: #cbd5e1;
        margin-top: 32px;
        line-height: 1.7;
    }


    /* =====================================================
   SIDEBAR RADIO NAVIGATION - LOOK LIKE CUSTOM MENU
===================================================== */

/* Container radio */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

/* Setiap item radio */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: transparent !important;
    border-radius: 12px !important;
    padding: 0px !important;
    margin: 0px 0px 4px 0px !important;
    min-height: 44px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

/* Isi label radio */
section[data-testid="stSidebar"] div[role="radiogroup"] label > div {
    padding: 12px 14px !important;
    border-radius: 12px !important;
    width: 100% !important;
}

/* Hover */
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover > div {
    background-color: rgba(255, 255, 255, 0.08) !important;
}

/* Item aktif */
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) > div {
    background-color: #0b5ba7 !important;
}

/* Teks menu */
section[data-testid="stSidebar"] div[role="radiogroup"] p {
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    line-height: 1.2 !important;
}

/* Hilangkan bulatan radio */
section[data-testid="stSidebar"] div[role="radiogroup"] input {
    display: none !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] svg {
    display: none !important;
}

/* Hilangkan wrapper bulatan radio Streamlit/BaseWeb */
section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

/* Pastikan teks tidak geser setelah bulatan dihilangkan */
section[data-testid="stSidebar"] div[role="radiogroup"] label > div:last-child {
    margin-left: 0px !important;
}


    /* =====================================================
       SIDEBAR FILTER LABELS
    ===================================================== */
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 700;
        font-size: 13px;
        margin-bottom: 4px;
    }


    /* =====================================================
       SIDEBAR MULTISELECT / SELECTBOX
    ===================================================== */
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #e5e7eb !important;
        min-height: 40px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #0f172a !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] input {
        color: #0f172a !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #0f172a !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #e0f2fe !important;
        color: #0f172a !important;
        border-radius: 8px !important;
        padding: 3px 6px !important;
        margin: 2px !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"] span {
        color: #0f172a !important;
        font-size: 12px !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"] svg {
        color: #0f172a !important;
        fill: #0f172a !important;
    }


    /* =====================================================
       DROPDOWN MENU LIST
    ===================================================== */
    div[data-baseweb="popover"] {
        z-index: 999999 !important;
    }

    div[data-baseweb="popover"] ul {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #e5e7eb !important;
        box-shadow: 0px 8px 24px rgba(15, 23, 42, 0.16) !important;
        padding-top: 6px !important;
        padding-bottom: 6px !important;
    }

    div[data-baseweb="popover"] li {
        color: #334155 !important;
        font-size: 14px !important;
        padding-top: 9px !important;
        padding-bottom: 9px !important;
    }

    div[data-baseweb="popover"] li:hover {
        background-color: #f1f5f9 !important;
    }


    /* =====================================================
       PAGE TITLE
    ===================================================== */
    .page-title {
        font-size: 38px;
        font-weight: 900;
        color: #0f172a;
        margin-bottom: 2px;
        letter-spacing: -0.4px;
    }

    .page-subtitle {
        font-size: 17px;
        color: #475569;
        margin-bottom: 22px;
    }


    /* =====================================================
       KPI METRIC CARDS
    ===================================================== */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px 18px;
        height: 125px;
        box-shadow: 0px 2px 8px rgba(15, 23, 42, 0.04);
    }

    .metric-title {
        font-size: 13px;
        color: #334155;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 900;
        color: #0f172a;
        line-height: 1.2;
        letter-spacing: 0.3px;
    }

    .metric-sub {
        font-size: 12px;
        color: #64748b;
        margin-top: 13px;
    }

    .metric-up {
        color: #16a34a;
        font-weight: 800;
    }

    .metric-down {
        color: #dc2626;
        font-weight: 800;
    }


    /* =====================================================
       CHART CARDS / CONTAINER
    ===================================================== */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        box-shadow: 0px 2px 8px rgba(15, 23, 42, 0.04);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 16px 16px 10px 16px;
    }

    .chart-title {
        font-size: 17px;
        font-weight: 900;
        color: #0f172a;
        margin-bottom: 4px;
    }

    .chart-subtitle {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 8px;
    }


    /* =====================================================
       INSIGHT BOX
    ===================================================== */
    .insight-box {
        background: #ecfeff;
        border: 1px solid #cffafe;
        border-radius: 16px;
        padding: 22px 24px;
        height: 100%;
        min-height: 310px;
        box-shadow: 0px 2px 8px rgba(15, 23, 42, 0.04);
    }

    .insight-title {
        color: #0f766e;
        font-size: 20px;
        font-weight: 900;
        margin-bottom: 14px;
    }

    .insight-box ul {
        padding-left: 18px;
        margin-top: 0;
        margin-bottom: 0;
    }

    .insight-box li {
        margin-bottom: 12px;
        color: #0f172a;
        font-size: 14px;
        line-height: 1.55;
    }


    /* =====================================================
       STREAMLIT BUTTONS
    ===================================================== */
    .stButton > button {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        color: #0f172a;
        font-weight: 700;
        padding: 0.55rem 1rem;
    }

    .stButton > button:hover {
        border-color: #0b5ba7;
        color: #0b5ba7;
    }


    /* =====================================================
       DATAFRAME / TABLE
    ===================================================== */
    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }


    /* =====================================================
       PLOTLY CHART SPACING
    ===================================================== */
    div[data-testid="stPlotlyChart"] {
        margin-top: -4px;
    }


    /* =====================================================
       SMALL RESPONSIVE ADJUSTMENT
    ===================================================== */
    @media (max-width: 1200px) {
        .metric-value {
            font-size: 22px;
        }

        .metric-title {
            font-size: 12px;
        }

        .page-title {
            font-size: 32px;
        }
    }

    </style>
    """,
        unsafe_allow_html=True,
    )

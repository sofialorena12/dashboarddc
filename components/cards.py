import streamlit as st

def metric_card(title, value, sub_text="vs previous period", delta_text=None, delta_type="up"):
    delta_class = "metric-up" if delta_type == "up" else "metric-down"
    delta_html = f"<span class='{delta_class}'>{delta_text}</span>" if delta_text else ""

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub_text} &nbsp; {delta_html}</div>
    </div>
    """, unsafe_allow_html=True)
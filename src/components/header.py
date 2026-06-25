import streamlit as st
import base64, os

def header_home():
    if os.path.exists("images/app_logo.png"):
        with open("images/app_logo.png", "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:65px;border-radius:14px;">'
    else:
        logo_html = '<div style="width:65px;height:65px;background:#FFD700;border-radius:14px;display:inline-flex;align-items:center;justify-content:center;font-size:34px;">🎓</div>'

    st.markdown(f"""
    <div style="text-align:center; margin-bottom:0.1rem; margin-top:0.2rem;">
        {logo_html}
    </div>
    <h1 style="
        font-family:'Outfit',sans-serif;
        font-weight:800;
        text-align:center;
        color:white;
        font-size:2rem;
        letter-spacing:-0.5px;
        margin-top:0.3rem;
        margin-bottom:0.6rem;
    ">Intelligent AI Attendance</h1>
    """, unsafe_allow_html=True)
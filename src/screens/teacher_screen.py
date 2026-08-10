import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    c1,c2 = st.columns(2, vertical_alignment= "center",gap = "xxlarge")
    with c1:
        header_dashboard()
    with c2:
        st.button("Go back to Home", type="secondary",key='loginbackbtn')


    st.header("Teacher Screen")

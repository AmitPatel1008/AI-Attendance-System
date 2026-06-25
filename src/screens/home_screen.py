import streamlit as st

from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home


def home_screen():
    style_base_layout()
    style_background_home()
    header_home()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("<h2>I'm<br>Student</h2>", unsafe_allow_html=True)
        # use_container_width=True + CSS height:200px gives equal size for both
        st.image("images/Student.png", use_container_width=True)
        if st.button("Student Portal ↗", key="student_btn"):
            st.session_state["login_type"] = "student"
            st.rerun()

    with col2:
        st.markdown("<h2>I'm<br>Teacher</h2>", unsafe_allow_html=True)
        st.image("images/Teacher.png", use_container_width=True)
        if st.button("Teacher Portal ↗", key="teacher_btn"):
            st.session_state["login_type"] = "teacher"
            st.rerun()

    footer_home()
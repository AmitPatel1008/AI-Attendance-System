import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen



def main():
    st.set_page_config(page_title="AI Attendance", page_icon="https://i.ibb.co/DgKSRjBY/app-logo.png")
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None :
            home_screen()
main()
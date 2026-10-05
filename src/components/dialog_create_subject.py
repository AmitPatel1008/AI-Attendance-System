import streamlit as st
from src.database.db import create_subject



@st.dialog("Create New Subject", icon="📚")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of the new subject below:")
    sub_id = st.text_input("Subject Code", placeholder="EC-601")
    sub_name = st.text_input("Subject Name", placeholder="DSA")
    sub_section = st.text_input("Section", placeholder="A")


    if st.button("Create Subject Now", type = 'primary', width = 'stretch'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.toast(f"Subject '{sub_name}' created successfully! 🎉")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating subject: {str(e)}")

        else:
            st.warning("⚠️ Please fill in all the fields to create a subject.")

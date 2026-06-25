import streamlit as st

def footer_home():
    st.markdown(
        """<div style="text-align:center;padding:12px 0 20px 0;font-family:Outfit,sans-serif;font-size:1.1rem;font-weight:700;color:white;line-height:2;">
        Made with &#10084;&#65039; by <span style="color:#A855F7;font-weight:900;">AMIT</span> <span style="color:#F59E0B;font-weight:900;">PATEL</span>
        </div>""",
        unsafe_allow_html=True
    )
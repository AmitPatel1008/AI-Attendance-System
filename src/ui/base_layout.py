import streamlit as st


def style_background_home():
    st.markdown("""
    <style>
    .stApp {
        background: #5865F2 !important;
        overflow: hidden !important;
        height: 100vh !important;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* No scroll - everything fits in viewport */
    .block-container {
        max-width: 780px !important;
        padding-top: 0.4rem !important;
        padding-bottom: 0rem !important;
        overflow: hidden !important;
    }

    /* Card columns - reduced padding */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        background: #D8DBFF !important;
        border-radius: 1.4rem !important;
        padding: 0.8rem 1rem 0.9rem 1rem !important;
        text-align: left !important;
    }

    /* Image: shorter height to save space */
    div[data-testid="stImage"] img {
        border-radius: 0.7rem !important;
        display: block !important;
        margin: 0 auto !important;
        width: 100% !important;
        height: 150px !important;
        object-fit: cover !important;
    }

    /* Button */
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        margin-top: 0.4rem !important;
    }
    div.stButton > button {
        background: #5865F2 !important;
        color: white !important;
        border: none !important;
        border-radius: 999px !important;
        font-weight: 700 !important;
        padding: 0.45rem 1.4rem !important;
        width: auto !important;
        font-size: 0.88rem !important;
        cursor: pointer !important;
        transition: background 0.2s ease, transform 0.15s ease !important;
    }
    div.stButton > button:hover {
        background: #4752C4 !important;
        color: white !important;
        transform: scale(1.05) !important;
        border: none !important;
    }
    div.stButton > button:active {
        transform: scale(0.97) !important;
        background: #3b45b0 !important;
        color: white !important;
    }
    div.stButton > button:focus {
        box-shadow: none !important;
        outline: none !important;
        color: white !important;
        border: none !important;
    }
    div.stButton > button:focus:not(:active) {
        background: #5865F2 !important;
        color: white !important;
    }

    h1 { color: white !important; text-align: center !important; }

    h2 {
        color: #1a1a1a !important;
        text-align: left !important;
        font-size: 1.3rem !important;
        margin-bottom: 0.3rem !important;
        margin-top: 0 !important;
        line-height: 1.0 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
    <style>
    .stApp { background: #E0E3FF !important; }
    </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    h1 {
        font-family: 'Outfit', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.6rem !important;
    }
    h2 {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.3rem !important;
        line-height: 1.0 !important;
    }
    h3, h4, p {
        font-family: 'Outfit', sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)
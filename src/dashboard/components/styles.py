import streamlit as st


def load_css():

    st.markdown("""
    <style>

    .stApp{
        background:
        linear-gradient(
            135deg,
            #020617,
            #0F172A,
            #1E1B4B
        );
    }

    .block-container{
        padding-top:2rem;
        padding-left:3rem;
        padding-right:3rem;
        max-width:100%;
    }

    h1{
        color:#F8FAFC;
        font-weight:700;
    }

    h2,h3,h4,h5{
        color:#E2E8F0;
    }

    p,label,span{
        color:#CBD5E1;
    }

    [data-testid="metric-container"]{
        background: rgba(15,23,42,0.55);
        backdrop-filter: blur(20px);
        border:1px solid rgba(255,255,255,0.08);
        border-radius:22px;
        padding:22px;
        box-shadow:
            0 8px 32px rgba(0,0,0,0.35);
        transition:0.3s;
    }

    [data-testid="metric-container"]:hover{
        transform:translateY(-3px);
        border:1px solid #3B82F6;
    }

    section[data-testid="stSidebar"]{
        background:
        linear-gradient(
            180deg,
            #020617,
            #111827
        );
    }

    div[data-testid="stDataFrame"]{
        border-radius:20px;
        overflow:hidden;
    }

    hr{
        border-color:#334155;
    }

    </style>
    """,
    unsafe_allow_html=True)
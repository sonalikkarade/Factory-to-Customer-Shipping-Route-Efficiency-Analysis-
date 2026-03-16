import streamlit as st

def navbar():

    st.markdown("""
    <style>

    .topnav{
    background: linear-gradient(90deg,#2563eb,#9333ea,#ec4899);
    padding:15px;
    border-radius:10px;
    text-align:center;
    font-size:22px;
    font-weight:bold;
    color:white;
    margin-bottom:25px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="topnav">🚚 Nassau Candy Logistics Analytics Platform</div>',
        unsafe_allow_html=True
    )
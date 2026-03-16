
import streamlit as st
def route_page(df):
 st.title("Route Efficiency")
 st.dataframe(df.groupby("State/Province")["Lead Time"].mean())

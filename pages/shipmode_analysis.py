
import streamlit as st, plotly.express as px
def shipmode_page(df):
 st.title("Ship Mode")
 fig=px.bar(df,x="Ship Mode",y="Lead Time")
 st.plotly_chart(fig,use_container_width=True)

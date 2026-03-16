import streamlit as st
import plotly.express as px

def dashboard_page(df):

    st.title("📊 Shipping Analytics Dashboard")

    if df.empty:
        st.warning("Dataset not loaded")
        return

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", len(df))
    col2.metric("Avg Lead Time", round(df["Lead Time"].mean(), 2))
    col3.metric("Total Sales", f"${df['Sales'].sum():,.0f}")
    col4.metric("Units Sold", int(df["Units"].sum()))

    st.markdown("---")

    fig = px.histogram(
        df,
        x="Lead Time",
        nbins=30,
        color_discrete_sequence=["#22c55e"]
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
from st_aggrid import AgGrid


# -------------------------
# LOAD BACKGROUND IMAGE
# -------------------------
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("background7.jpg")

# -------------------------
# CUSTOM CSS
# -------------------------
st.markdown(
f"""
<style>

#MainMenu {{visibility:hidden;}}
footer {{visibility:hidden;}}
header {{visibility:hidden;}}
[data-testid="stSidebar"] {{display:none;}}

.stApp {{
background-image: url("data:image/png;base64,{bg}");
background-size: cover;
background-position: center;
background-attachment: fixed;
}}

.dashboard-title {{
font-size:42px;
font-weight:700;
color:#00E5FF;
text-align:center;
margin-bottom:25px;
text-shadow:0px 0px 20px #00E5FF;
}}

.glass {{
background:rgba(10,15,35,0.75);
backdrop-filter: blur(12px);
padding:20px;
border-radius:16px;
box-shadow:0px 0px 25px rgba(0,0,0,0.6);
}}

.kpi-card {{
background:rgba(20,25,60,0.85);
padding:20px;
border-radius:14px;
text-align:center;
box-shadow:0 0 20px rgba(0,229,255,0.4);
}}

.kpi-value {{
font-size:28px;
font-weight:bold;
color:#00E5FF;
}}

.kpi-label {{
font-size:14px;
color:#A5B4FC;
}}

</style>
""",
unsafe_allow_html=True
)

# -------------------------
# TITLE
# -------------------------
st.markdown(
'<div class="dashboard-title">🚚 Factory → Customer Shipping Analytics</div>',
unsafe_allow_html=True
)

# -------------------------
# GENERATE SAMPLE DATA
# -------------------------
np.random.seed(42)

states = ["CA","TX","NY","FL","WA","IL","AZ"]
regions = ["West","Central","East"]

df = pd.DataFrame({
"State":np.random.choice(states,600),
"Region":np.random.choice(regions,600),
"Ship_Mode":np.random.choice(["Standard","Express","Same Day"],600),
"Lead_Time":np.random.randint(1,8,600),
"Sales":np.random.randint(100,1000,600)
})

# -------------------------
# KPI CARDS
# -------------------------
c1,c2,c3,c4 = st.columns(4)

c1.markdown(f"""
<div class="kpi-card">
<div class="kpi-value">{len(df)}</div>
<div class="kpi-label">Total Shipments</div>
</div>
""", unsafe_allow_html=True)

c2.markdown(f"""
<div class="kpi-card">
<div class="kpi-value">{round(df["Lead_Time"].mean(),2)}</div>
<div class="kpi-label">Avg Lead Time</div>
</div>
""", unsafe_allow_html=True)

c3.markdown(f"""
<div class="kpi-card">
<div class="kpi-value">${df["Sales"].sum()}</div>
<div class="kpi-label">Total Sales</div>
</div>
""", unsafe_allow_html=True)

delay_rate = len(df[df["Lead_Time"]>5]) / len(df) * 100

c4.markdown(f"""
<div class="kpi-card">
<div class="kpi-value">{round(delay_rate,1)}%</div>
<div class="kpi-label">Delay Rate</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------------
# CHARTS ROW
# -------------------------
col1,col2 = st.columns(2)

with col1:

   state_perf = df.groupby(["State","Region"])["Lead_Time"].mean().reset_index()
fig = px.bar(
    state_perf,
    x="State",
    y="Lead_Time",
    color="Region",
    animation_frame="Region",
    color_discrete_sequence=["#00E5FF","#FF4ECD","#7B2FF7"]
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, width="stretch")

with col2:

    ship_perf = df.groupby(["Ship_Mode","Region"])["Lead_Time"].mean().reset_index()

fig2 = px.pie(
    ship_perf,
    names="Ship_Mode",
    values="Lead_Time",
    hole=0.6,
    color_discrete_sequence=["#00E5FF","#FF4ECD","#7B2FF7"]
)

fig2.update_layout(template="plotly_dark")

st.plotly_chart(fig2, width="stretch")

# -------------------------
# SALES TREND
# -------------------------
st.write("")

trend = df.groupby(["State","Region"])["Sales"].sum().reset_index()

fig3 = px.line(
    trend,
    x="State",
    y="Sales",
    color="Region",
    markers=True,
    animation_frame="Region",
    color_discrete_sequence=["#00E5FF","#FF4ECD","#7B2FF7"]
)

fig3.update_layout(
    template="plotly_dark",
    title="Sales Trend",
    transition_duration=1000
)

st.plotly_chart(fig3, width="stretch")

# -------------------------
# ROUTE EFFICIENCY TABLE
# -------------------------
st.write("")

route = df.groupby(["Region","State"]).agg(
Shipments=("State","count"),
Avg_Lead_Time=("Lead_Time","mean")
).reset_index()

map_data = df.groupby("State")["Sales"].sum().reset_index()

fig_map = px.choropleth(
    map_data,
    locations="State",
    locationmode="USA-states",
    color="Sales",
    scope="usa",
    color_continuous_scale="Turbo"
)

fig_map.update_layout(template="plotly_dark")


AgGrid(
    route,
    theme="alpine-dark",
    height=350,
    fit_columns_on_grid_load=True
)
st.set_page_config(layout="wide")


st.plotly_chart(fig_map, width="stretch")

route = route.sort_values("Avg_Lead_Time")

st.dataframe(route, width="stretch")

import plotly.express as px

fig = px.choropleth(
    state_data,
    locations="State",
    locationmode="USA-states",
    color="Lead_Time",
    scope="usa"
)
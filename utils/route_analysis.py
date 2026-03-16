def route_efficiency(df):

    route_summary = df.groupby("Route").agg(
        total_shipments=("Order ID","count"),
        avg_lead_time=("Lead_Time","mean"),
        lead_time_std=("Lead_Time","std")
    ).reset_index()

    route_summary["efficiency_score"] = 1 / route_summary["avg_lead_time"]

    route_summary = route_summary.sort_values("avg_lead_time")

    return route_summary
import pandas as pd

def load_data():

    df = pd.read_csv("data/shipping_data.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

    df = df.dropna(subset=["Ship Date","Order Date"])

    return df
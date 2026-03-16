import pandas as pd

def create_features(df):

    df["Lead_Time"] = (df["Ship Date"] - df["Order Date"]).dt.days

    df = df[df["Lead_Time"] >= 0]

    df["Route"] = df["Division"] + " → " + df["State/Province"]

    return df
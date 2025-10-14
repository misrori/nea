import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



def kizart():
    st.title("Kizárt projektek")
    # Read data
    df = pd.read_csv("/home/mihaly/python_codes/nea/nea_data.csv")
    # drop the first column
    df = df.iloc[:, 1:]

    # If needed, rename columns only if there are exactly 5 columns
    expected_cols = ["Név", "Azonosító", "Igényelt támogatás", "Státusz", "Kizárás"]
    df.columns = expected_cols
    df["Igényelt támogatás"] = df["Igényelt támogatás"].replace({" " : ""}, regex=True).astype(int)
    df.sort_values("Igényelt támogatás", inplace=True)

    st.dataframe(df)

    # for each unique status generate a plotly plot where you grupb by Név and calculate tne nomber of rows and sum of Igényelt támogatás
    grouped = (df
        .groupby(["Név", "Státusz"])
        .agg(
            projekt_szam=("Név", "count"),
            tamogatas_osszesen=("Igényelt támogatás", "sum")
        )
        .reset_index()
        .rename(columns={"projekt_szam": "Projekt szám", "tamogatas_osszesen": "Támogatás összesen"})
    )
    grouped.sort_values("Támogatás összesen", inplace=True, ascending=False)
    # format large numbers in column "Támogatás összesen" with spaces as thousand separators
    grouped["Támogatás összesen"] = grouped["Támogatás összesen"].apply(lambda x: f"{x:,}".replace(",", " "))   

    st.dataframe(grouped)


kizart()
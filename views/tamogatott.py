import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def supported():
    st.title("Támogatott projektek")
    # Read data
    df = pd.read_csv("nea_data.csv")
    # drop the first column
    df = df.iloc[:, 1:]

    # If needed, rename columns only if there are exactly 5 columns
    expected_cols = ["Név", "Azonosító", "Igényelt támogatás", "Státusz", "Kizárás"]
    df.columns = expected_cols
    df["Név"] = df["Név"].str.strip()

    df["Igényelt támogatás"] = df["Igényelt támogatás"].replace({" " : ""}, regex=True).astype(int)
    df.sort_values("Igényelt támogatás", inplace=True)
    df.reset_index(drop=True, inplace=True)

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
    grouped.reset_index(drop=True, inplace=True)

    st.title("Összesítés név és státusz szerint")
    
    st.dataframe(grouped)

    st.title("Kizárt projektek")

    kizart_df_agg = (df
        .groupby(["Név", "Kizárás"])
        .agg(
            kizart_projektek__szama=("Név", "count"),
        )
        .reset_index()
        .rename(columns={"kizart_projektek__szama": "Kizárt projektek száma"})
    )
    kizart_df_agg.reset_index(drop=True, inplace=True)
    st.dataframe(kizart_df_agg)


supported()
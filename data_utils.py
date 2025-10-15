import streamlit as st
import pandas as pd

@st.cache_data
def load_nea_data():
    df = pd.read_csv("nea_data.csv")
    df = df.iloc[:, 1:]
    expected_cols = ["Név", "Azonosító", "Igényelt támogatás", "Státusz", "Kizárás"]
    df.columns = expected_cols
    df["Név"] = df["Név"].str.strip()
    df["Igényelt támogatás"] = df["Igényelt támogatás"].replace({" " : ""}, regex=True).astype(int)
    df.sort_values("Igényelt támogatás", inplace=True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    return df

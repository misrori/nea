import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_utils import load_nea_data



def supported():
    df = load_nea_data()

    col1, col2 = st.columns(2)
    with col1:
        #text filter for name
        name_filter = st.text_input("Név szűrés (szöveg)", "")
    with col2:
        azonosito_filter = st.text_input("Azonosító szűrés (szöveg)", "")
    if name_filter:
        df = df[df["Név"].str.contains(name_filter, case=False)]
    if azonosito_filter:
        df = df[df["Azonosító"].astype(str).str.contains(azonosito_filter, case=False)]

    # filter for támogatás with a slicer
    min_tamogatas, max_tamogatas = int(df["Igényelt támogatás"].min()), int(df["Igényelt támogatás"].max())
    tamogatas_range = st.slider("Igényelt támogatás szűrés", min_value=min_tamogatas, max_value=max_tamogatas, value=(min_tamogatas, max_tamogatas), step=100000)
    df = df[(df["Igényelt támogatás"] >= tamogatas_range[0]) & (df["Igényelt támogatás"] <= tamogatas_range[1])]

    # multiple choice for státusz and kizárás
    status_options = df["Státusz"].unique().tolist()
    #selected_status = st.multiselect("Státusz", options=status_options, default="Nyertes")
    selected_status = st.multiselect("Státusz", options=status_options, default=status_options)

    exclusion_options = ["Igen", "Nem"]
    selected_exclusion = st.multiselect("Kizárás", options=exclusion_options, default=exclusion_options)
    # filter the dataframe based on the selections
    df = df[df["Státusz"].isin(selected_status) & df["Kizárás"].isin(selected_exclusion)]
    if df.empty:
        st.warning("Nincsenek projektek az adatok között a szűrők alapján.")
        return

    # Show all data
    st.title("Összes adat")
    
    # download button for the dataframe
    st.download_button(
        label="Összes adat letöltése CSV-ben",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='nea_data.csv',
        mime='text/csv',
    )
    df_to_show = df.copy()
    df_to_show.reset_index(drop=True, inplace=True)
    df_to_show["Igényelt támogatás"] = df_to_show["Igényelt támogatás"].apply(lambda x: f"{x:,}".replace(",", " "))
    st.dataframe(df_to_show)


    #Név, Státusz szerint összesítés
    grouped = (df
        .groupby(["Név", "Státusz"])
        .agg(
            tamogatas_osszesen=("Igényelt támogatás", "sum"),
            projekt_szam=("Név", "count")
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


supported()
import streamlit as st
import pandas as pd
from data_utils import load_nea_data



def kizart():
    df = load_nea_data()
    df = df[df["Kizárás"]=='Igen']
    if df.empty:
        st.warning("Nincsenek kizárt projektek az adatok között.")
        return
    else:
        st.title("Kizárt projektek")
        # download button for the dataframe
        st.download_button(
            label="Kizárt projektek letöltése CSV-ben",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='kizart_nea_data.csv',
            mime='text/csv',
        )
        df_to_show = df.copy()
        df_to_show["Igényelt támogatás"] = df_to_show["Igényelt támogatás"].apply(lambda x: f"{x:,}".replace(",", " "))
        st.dataframe(df_to_show)    

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


kizart()
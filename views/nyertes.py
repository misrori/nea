import streamlit as st
import pandas as pd
from data_utils import load_nea_data



def nyertes():
    df = load_nea_data()
    df = df[df["Státusz"]=='Nyertes']
    if df.empty:
        st.warning("Nincsenek nyertes projektek az adatok között.")
        return
    else:
        st.title("Nyertes projektek")
        # download button for the dataframe
        st.download_button(
            label="Nyertes projektek letöltése CSV-ben",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='nyertes_nea_data.csv',
            mime='text/csv',
        )
        df_to_show = df.copy()
        df_to_show["Igényelt támogatás"] = df_to_show["Igényelt támogatás"].apply(lambda x: f"{x:,}".replace(",", " "))
        df_to_show.reset_index(drop=True, inplace=True)
        st.title("Részletes adatok")
        
        st.dataframe(df_to_show)    

        nyertes_df_agg = (df
            .groupby("Név")
            .agg(
                elnyert_tamogatás_összege=("Igényelt támogatás", "sum"),
                nyertes_projektek__szama=("Név", "count"),
            )
            .sort_values(by="elnyert_tamogatás_összege", ascending=False)
            #.reset_index()
            .rename(columns={"elnyert_tamogatás_összege": "Elnyert támogatás összege", 
                             "nyertes_projektek__szama": "Nyertes projektek száma"})
        )
        nyertes_df_agg.reset_index(drop=True, inplace=True)
        top20_nyertes = nyertes_df_agg.head(20).copy()
        nyertes_df_agg["Elnyert támogatás összege"] = nyertes_df_agg["Elnyert támogatás összege"].apply(lambda x: f"{x:,}".replace(",", " "))
        st.title("Összesítés név szerint")
        st.dataframe(nyertes_df_agg)

        # top 20 nyertes in plotly
        import plotly.express as px
        # show the money in million huf
        top20_nyertes['Elnyert támogatás összege'] = top20_nyertes['Elnyert támogatás összege']/ 1_000_000

        fig = px.bar(top20_nyertes, 
                     y="Név", 
                     x="Elnyert támogatás összege", 
                     title="Top 20 nyertes támogatottak név szerint",
                     labels={"Név": "Név", "Elnyert támogatás összege": "Elnyert támogatás összege (Millió HUF)"},
                     text="Elnyert támogatás összege"
                    )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(yaxis_tickformat = ',')
        # set height 1000 px
        fig.update_layout(height=1000)
        # set the order to decreasing
        fig.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True)


nyertes()
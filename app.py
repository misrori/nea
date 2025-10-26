import streamlit as st


st.set_page_config( layout="wide", page_title="NEA",page_icon="💰")



# --- INTRO ---
supported_site = st.Page(
    "views/tamogatott.py",
    title="Támogatott projektek",
    icon=":material/account_circle:",
    default=True,
)

kizart_site = st.Page(
    "views/kizart.py",
    title="Kizart projektek",
    icon=":material/trending_up:",
)

nyertes_site = st.Page(
    "views/nyertes.py",
    title="Nyertes projektek",
    icon=":material/star:",
)




pg = st.navigation(
    {
        "Összes projektek": [supported_site],
        "Nyertes projektek": [nyertes_site],
                "Kizárt projektek": [kizart_site]
    }
)


# --- SHARED ON ALL PAGES ---
st.logo(
    'https://atlatszo.hu/wp-content/themes/atlatszo2021/i/favicon.svg',
    link="https://atlatszo.hu",
    size="large")

st.sidebar.markdown("Szeretettel ❤️ by [Atlatszo](https://atlatszo.hu)")


# --- RUN NAVIGATION ---
pg.run()
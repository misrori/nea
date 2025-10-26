import streamlit as st
import pandas as pd

# cashe data for 1 hour
@st.cache_data(ttl=3600)
def load_nea_data():
    df = pd.read_csv("nea.csv")
    df = df.iloc[:, 1:]
    expected_cols = ["Név", "Azonosító", "Igényelt támogatás", "Státusz", "Kizárás"]
    df.columns = expected_cols
    df["Név"] = df["Név"].str.strip()
    df["Státusz"] = df["Státusz"].str.strip()
    # remowe the startin " 
    df["Név"] = df["Név"].str.replace(r'^"', '', regex=True)

    #remowe all "
    df["Név"] = df["Név"].str.replace(r'"', '', regex=True)

    df["Igényelt támogatás"] = df["Igényelt támogatás"].replace({" " : ""}, regex=True).astype(int)

    status_map = {
        # Érvénytelen / invalid cases
        "érvénytelen": "Érvénytelen",
        "Érvénytelen": "Érvénytelen",
        "Érvénytelen, értesítve": "Érvénytelen",

        # Lezárt / closed cases
        "lezárt": "Lezárt",
        "Lezárt": "Lezárt",

        # Várólistás / waiting list
        "várólistás": "Várólistás",
        "Várólistás": "Várólistás",

        # Elutasított / rejected
        "elutasított": "Elutasított",
        "Elutasított": "Elutasított",

        # Lemondott / withdrawn
        "lemondott": "Lemondott",
        "Lemondott": "Lemondott",

        # Nyertes / winner
        "nyertes": "Nyertes",
        "Nyertes": "Nyertes",

        # Nem támogatott / not supported
        "nem támogatott": "Nem támogatott",
        "Nem támogatott": "Nem támogatott",

        # Nem befogadható / not admissible
        "Nem befogadható": "Nem befogadható",
        "Nem befogadható ": "Nem befogadható",
        "Nem fogadható be": "Nem befogadható",
        "Nem fogadható be, értesítve": "Nem befogadható",

        # Szerződéskötés meghiúsult / contract failed
        "szerződéskötés meghiúsult": "Szerződéskötés meghiúsult",
        "Szerződéskötés meghiúsult": "Szerződéskötés meghiúsult",

        # Szerződéskötés alatt / under contract
        "Szerződéskötés alatt": "Szerződéskötés alatt",

        # Szerződéskötési hiánypótlás alatt / missing documents
        "Szerződéskötési hiánypótlás alatt": "Szerződéskötési hiánypótlás alatt",

        # Visszavonás / withdrawal
        "részösszeg visszavonás": "Visszavonás",
        "teljes összeg visszavonás": "Visszavonás",

        # Beérkezett / received
        "Beérkezett": "Beérkezett",
    }
    df["Státusz_clean"] = df["Státusz"].map(status_map)
    df['Státusz'] = df['Státusz_clean']
    df.drop(columns=['Státusz_clean'], inplace=True)



    df.sort_values("Igényelt támogatás", inplace=True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    return df

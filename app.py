import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(page_title="Football AI Pro", page_icon="⚽", layout="wide")

st.title("⚽ Football AI Pro")
st.write("Gratis fotbollsanalys med historisk matchdata")

st.sidebar.header("Meny")
page = st.sidebar.radio(
    "Välj sida",
    ["Matchanalys", "Importera matchdata", "Databas"]
)

# -----------------------------
# IMPORTERA MATCHDATA
# -----------------------------
if page == "Importera matchdata":
    st.header("📥 Importera gratis matchdata")

    st.write(
        "Ladda upp en CSV-fil med historiska fotbollsmatcher. "
        "Du kan hämta gratis filer från Football-Data.co.uk."
    )

    uploaded_file = st.file_uploader("Välj CSV-fil", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            st.success("Filen har laddats upp!")
            st.write("Förhandsvisning:")
            st.dataframe(df.head(20), use_container_width=True)

            if "HomeTeam" in df.columns and "AwayTeam" in df.columns:
                st.session_state["football_data"] = df
                st.success(f"{len(df)} matcher har importerats!")
            else:
                st.error(
                    "Filen saknar kolumnerna HomeTeam och AwayTeam."
                )

        except Exception as e:
            st.error(f"Kunde inte läsa filen: {e}")

# -----------------------------
# MATCHANALYS
# -----------------------------
elif page == "Matchanalys":
    st.header("🔍 Automatisk matchanalys")

    df = st.session_state.get("football_data")

    if df is None:
        st.info("Importera först en CSV-fil under Importera matchdata.")

    else:
        teams = sorted(
            set(df["HomeTeam"].dropna()).union(
                set(df["AwayTeam"].dropna())
            )
        )

        col1, col2 = st.columns(2)

        with col1:
            home = st.selectbox("Hemmalag", teams)

        with col2:
            away = st.selectbox(
                "Bortalag",
                [team for team in teams if team != home]
            )

        if st.button("Analysera match"):
            home_games = df[df["HomeTeam"] == home]
            away_games = df[df["AwayTeam"] == away]

            home_goals = pd.to_numeric(
                home_games.get("FTHG"), errors="coerce"
            ).mean()

            away_goals = pd.to_numeric(
                away_games.get("FTAG"), errors="coerce"
            ).mean()

            home_conceded = pd.to_numeric(
                home_games.get("FTAG"), errors="coerce"
            ).mean()

            away_conceded = pd.to_numeric(
                away_games.get("FTHG"), errors="coerce"
            ).mean()

            if pd.isna(home_goals) or pd.isna(away_goals):
                st.error("Det finns inte tillräckligt med resultatdata.")
            else:
                expected_home = (home_goals + away_conceded) / 2
                expected_away = (away_goals + home_conceded) / 2

                st.subheader("📊 Förväntade mål")
                c1, c2 = st.columns(2)
                c1.metric(home, round(expected_home, 2))
                c2.metric(away, round(expected_away, 2))

                st.subheader("🎯 Enkel målprognos")

                total = expected_home + expected_away

                if total > 2.5:
                    st.success("Modellens indikation: Över 2,5 mål")
                else:
                    st.info("Modellens indikation: Under 2,5 mål")

                if expected_home > expected_away:
                    st.write(f"Modellen lutar åt seger för {home}.")
                elif expected_away > expected_home:
                    st.write(f"Modellen lutar åt seger för {away}.")
                else:
                    st.write("Modellen bedömer lagen som jämna.")

                st.caption(
                    "Prognosen bygger på genomsnittliga historiska "
                    "mål och är inte en garanti."
                )

# -----------------------------
# DATABAS
# -----------------------------
elif page == "Databas":
    st.header("🗄️ Matchdatabas")

    df = st.session_state.get("football_data")

    if df is None:
        st.info("Ingen data importerad ännu.")
    else:
        st.metric("Importerade matcher", len(df))
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Ladda ner databasen",
            data=csv,
            file_name="football_database.csv",
            mime="text/csv"
        )

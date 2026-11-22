import streamlit as st
import pandas as pd
import numpy as np
import math
import json
import os

st.set_page_config(
    page_title="Football AI Pro",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FOOTBALL AI PRO")
st.caption("Advanced Football Prediction Engine")

FILE = "football_data.json"

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {"teams": {}, "matches": []}

data = load_data()

def save_data():
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def poisson(k, lam):
    return (lam ** k) * math.exp(-lam) / math.factorial(k)

def analyze(home, away, hg, ag):
    matrix = np.zeros((9, 9))

    for i in range(9):
        for j in range(9):
            matrix[i, j] = poisson(i, hg) * poisson(j, ag)

    home_win = np.tril(matrix, -1).sum()
    draw = np.trace(matrix)
    away_win = np.triu(matrix, 1).sum()

    over15 = sum(matrix[i, j] for i in range(9)
                 for j in range(9) if i+j > 1)
    over25 = sum(matrix[i, j] for i in range(9)
                 for j in range(9) if i+j > 2)
    over35 = sum(matrix[i, j] for i in range(9)
                 for j in range(9) if i+j > 3)

    btts = sum(matrix[i, j] for i in range(1, 9)
               for j in range(1, 9))

    return {
        "1": home_win,
        "X": draw,
        "2": away_win,
        "Over 1.5": over15,
        "Over 2.5": over25,
        "Over 3.5": over35,
        "BTTS": btts
    }

def percentage(x):
    return f"{x * 100:.1f}%"

st.sidebar.title("⚙️ Navigation")

page = st.sidebar.radio(
    "Choose section",
    ["Match Analysis", "Team Database", "Match History"]
)

if page == "Match Analysis":

    st.header("🔎 Advanced Match Analysis")

    teams = list(data["teams"].keys())

    home = st.text_input("Home Team", "Arsenal")
    away = st.text_input("Away Team", "Chelsea")

    st.subheader("Team statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.write("HOME TEAM")
        home_scored = st.number_input(
            "Average goals scored",
            min_value=0.0, value=1.7, step=0.1
        )
        home_conceded = st.number_input(
            "Average goals conceded",
            min_value=0.0, value=1.0, step=0.1
        )
        home_corners = st.number_input(
            "Average corners",
            min_value=0.0, value=5.5, step=0.5
        )
        home_shots = st.number_input(
            "Average shots",
            min_value=0.0, value=13.0, step=1.0
        )

    with col2:
        st.write("AWAY TEAM")
        away_scored = st.number_input(
            "Away goals scored",
            min_value=0.0, value=1.3, step=0.1
        )
        away_conceded = st.number_input(
            "Away goals conceded",
            min_value=0.0, value=1.4, step=0.1
        )
        away_corners = st.number_input(
            "Away corners",
            min_value=0.0, value=4.5, step=0.5
        )
        away_shots = st.number_input(
            "Away shots",
            min_value=0.0, value=10.0, step=1.0
        )

    if st.button("🚀 ANALYZE MATCH", use_container_width=True):

        if home.strip().lower() == away.strip().lower():
            st.error("Choose two different teams.")
        else:
            expected_home = max(
                0.05, (home_scored + away_conceded) / 2
            )
            expected_away = max(
                0.05, (away_scored + home_conceded) / 2
            )

            results = analyze(
                home, away, expected_home, expected_away
            )

            st.success(f"{home} vs {away}")

            st.subheader("📊 1X2 Predictions")

            c1, c2, c3 = st.columns(3)

            c1.metric("Home Win", percentage(results["1"]))
            c2.metric("Draw", percentage(results["X"]))
            c3.metric("Away Win", percentage(results["2"]))

            st.subheader("⚽ Goal Predictions")

            for key in ["Over 1.5", "Over 2.5", "Over 3.5", "BTTS"]:
                st.write(f"{key}: {percentage(results[key])}")

            st.subheader("🎯 Expected Goals (xG)")

            c1, c2 = st.columns(2)
            c1.metric(home, f"{expected_home:.2f}")
            c2.metric(away, f"{expected_away:.2f}")

            st.subheader("🚩 Corner Prediction")

            total_corners = home_corners + away_corners
            st.metric("Expected Total Corners", f"{total_corners:.1f}")

            st.subheader("🥅 Shot Prediction")

            total_shots = home_shots + away_shots
            st.metric("Expected Total Shots", f"{total_shots:.1f}")

            st.info(
                "Predictions are statistical estimates based on "
                "the entered team averages, not guaranteed outcomes."
            )

            data["matches"].append({
                "home": home,
                "away": away,
                "home_xg": expected_home,
                "away_xg": expected_away,
                "predictions": results
            })

            save_data()

elif page == "Team Database":

    st.header("📚 Team Database")

    team = st.text_input("Team name")

    scored = st.number_input(
        "Goals scored per match", min_value=0.0, value=1.5
    )

    conceded = st.number_input(
        "Goals conceded per match", min_value=0.0, value=1.0
    )

    if st.button("Save Team"):
        if team.strip():
            data["teams"][team] = {
                "scored": scored,
                "conceded": conceded
            }
            save_data()
            st.success("Team saved!")

    if data["teams"]:
        st.dataframe(pd.DataFrame(data["teams"]).T)

elif page == "Match History":

    st.header("📈 Match History")

    if data["matches"]:
        history = pd.DataFrame(data["matches"])
        st.dataframe(history, use_container_width=True)
    else:
        st.info("No analyzed matches yet.")

st.divider()

st.caption("FOOTBALL AI PRO | Advanced Engine v2.0")

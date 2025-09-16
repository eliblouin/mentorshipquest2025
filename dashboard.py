"""
Name:       Quest Dashboard
Description:
This dashboard provides users with up-to-date information on the current standings of FALL 2025 quest pairings. It also
"""
import pandas as pd
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import webbrowser
from PIL import Image

register_url = "https://forms.gle/nqgbBFfeuBTQsXBPA"
submit_url = "https://forms.gle/J3cpLXXRBZG9Pdoc8"

def website_setup(df, colork = 'yellow'):
    # [PY5] A dictionary where you write code to access its keys, values, or items
    colors = {'yellow':'#FEFBD4', 'blue':'#D5FBFD', 'pink':'#FDE9FF', 'orange':'#FEE8D9', 'green':'#E5FED9'}
    # [ST4] Customized page design features (sidebar, fonts, colors, images, navigation)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {colors[colork]};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("🏆 Mission: Mentorship Dashboard")
    st.link_button("Register Your Team", register_url)
    st.link_button("Submit a Challenge", submit_url)
    st.text("Updated on 9/5/2025 at 7:50PM EST")
    img = Image.open("mentorship.png")
    st.image(img, width=700)
    # Load CSV
    df = pd.read_csv("quest_results.csv")

    # Create "Students" column by combining Student1 and Student2
    # Use only first names
    df["Student1_first"] = df["Member 1"].str.split().str[0]
    df["Student2_first"] = df["Member 2"].str.split().str[0]

    # Create "Students" column with first names only
    df["Students"] = df["Student1_first"] + " & " + df["Student2_first"]

    # Check for necessary columns
    required_cols = {"Name", "Points"}

    # Aggregate total points by team
    team_points = df.groupby(["Name", "Students"])["Points"].sum().reset_index()
    team_points = team_points.sort_values(by="Points", ascending=False).reset_index(drop=True)
    team_points.index = team_points.index + 1

    # Highlight leaderboard
    st.subheader("Leaderboard (Top 10 Teams)")
    leaderboard = team_points.head(10).copy()
    leaderboard.index.name = "Rank"
    st.table(leaderboard[["Name", "Students", "Points"]])

    # Show full table
    st.subheader("Total Points per Team")
    team_points_display = team_points.copy()
    team_points_display.index.name = "Rank"
    st.dataframe(team_points_display[["Name", "Students", "Points"]])

    # Challenge distribution pie chart
    st.subheader("Challenge Completion Distribution")

    challenge_counts = df["Challenge"].value_counts()

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)  # transparent figure background
    ax.set_facecolor("none")  # transparent axes background

    # Create N yellow shades based on number of challenges
    n = len(challenge_counts)
    colors = cm.YlOrBr(np.linspace(0.4, 1, n))  # yellow to darker golden-brown

    ax.pie(
        challenge_counts,
        labels=challenge_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors
    )
    ax.axis("equal")  # Equal aspect ratio for circle
    st.pyplot(fig)


def main():
    df = 'quest_results.csv'
    website_setup(df)

if __name__ == "__main__":
    main()


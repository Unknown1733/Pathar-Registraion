import streamlit as st
import pandas as pd
import base64
import io
from PIL import Image

st.set_page_config(layout="centered", page_title="Pathar Premier League")

st.title("Pathar Tennis Ball Premier League - Player Registration")

# Initialize session state
if 'players' not in st.session_state:
    st.session_state.players = []

# Player registration form
with st.form("player_form"):
    st.subheader("Enter Player Details")
    name = st.text_input("Player Name")
    village = st.text_input("Village")
    category = st.selectbox("Category", ["All Rounder", "Batsman", "Bowler"])
    tshirt_size = st.text_input("T-Shirt Size")
    mobile = st.text_input("Mobile Number")
    photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Submit")

    if submitted:
        if name and village and mobile:
            st.session_state.players.append({
                "Name": name,
                "Village": village,
                "Category": category,
                "T-Shirt Size": tshirt_size,
                "Mobile": mobile,
                "Photo": photo.read() if photo else None
            })
            st.success(f"{name} registered successfully!")
        else:
            st.warning("Please fill all required fields!")

# Show registered players
if st.session_state.players:
    st.header("Registered Players")

    data = []
    for player in st.session_state.players:
        st.markdown(f"*Name:* {player['Name']}")
        st.markdown(f"*Village:* {player['Village']}")
        st.markdown(f"*Category:* {player['Category']}")
        st.markdown(f"*T-Shirt Size:* {player['T-Shirt Size']}")
        st.markdown(f"*Mobile:* {player['Mobile']}")
        if player['Photo']:
            st.image(player['Photo'], width=120)
        st.markdown("---")
        data.append({
            "Name": player["Name"],
            "Village": player["Village"],
            "Category": player["Category"],
            "T-Shirt Size": player["T-Shirt Size"],
            "Mobile": player["Mobile"]
        })

    df = pd.DataFrame(data)

    # Download as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data as CSV", csv, "players.csv", "text/csv")

    # Download as Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Players')
    st.download_button("Download Data as Excel", output.getvalue(), "players.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
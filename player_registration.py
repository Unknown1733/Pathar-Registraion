import streamlit as st
import pandas as pd
import base64
import io
import os
from PIL import Image

st.set_page_config(layout="centered", page_title="Pathar Premier League")

st.title("Pathar Tennis Ball Premier League - Player Registration")

# Initialize session state
if 'players' not in st.session_state:
    st.session_state.players = []
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Create photos folder if it doesn't exist
if not os.path.exists("photos"):
    os.makedirs("photos")

# Only show form if not submitted
if not st.session_state.submitted:
    with st.form("player_form"):
        st.subheader("Enter Player Details")
        name = st.text_input("Player Name")
        village = st.text_input("Village")
        category = st.selectbox("Category", ["All Rounder", "Batsman", "Bowler", "Wicket Keeper"])
        tshirt_size = st.selectbox("T-Shirt Size", ["S", "M", "L", "XL", "XXL"])
        mobile = st.text_input("Mobile Number")
        photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("Submit")

        if submitted:
            if name and village and mobile:
                # Save player data
                st.session_state.players.append({
                    "Name": name,
                    "Village": village,
                    "Category": category,
                    "T-Shirt Size": tshirt_size,
                    "Mobile": mobile,
                    "Photo": f"{name}_{village}.jpg" if photo else None
                })

                # Save photo to 'photos' folder
                if photo:
                    image = Image.open(photo)
                    photo_path = f"photos/{name}_{village}.jpg"
                    image.save(photo_path)

                # Save to CSV
                df = pd.DataFrame(st.session_state.players)
                df.to_csv("players_data.csv", index=False)

                st.success(f"{name} registered successfully!")
                st.session_state.submitted = True
            else:
                st.warning("Please fill all required fields!")

else:
    st.success("Registration Successful! Thank you.")
    st.button("Register Another Player", on_click=lambda: st.session_state.update({"submitted": False}))

# Show registered players
if st.session_state.players:
    st.header("Registered Players")

    for player in st.session_state.players:
        st.markdown(f"*Name:* {player['Name']}")
        st.markdown(f"*Village:* {player['Village']}")
        st.markdown(f"*Category:* {player['Category']}")
        st.markdown(f"*T-Shirt Size:* {player['T-Shirt Size']}")
        st.markdown(f"*Mobile:* {player['Mobile']}")
        if player['Photo'] and os.path.exists(f"photos/{player['Photo']}"):
            st.image(f"photos/{player['Photo']}", width=120)
        st.markdown("---")

    # Download as CSV
    df = pd.DataFrame(st.session_state.players)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data as CSV", csv, "players.csv", "text/csv")

    # Download as Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Players')
    st.download_button("Download Data as Excel", output.getvalue(), "players.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

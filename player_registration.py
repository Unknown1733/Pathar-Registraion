import streamlit as st
import pandas as pd
import base64
import io
import os
from PIL import Image

st.set_page_config(layout="centered", page_title="Pathar Premier League")

st.title("Pathar Tennis Ball Premier League - Player Registration")

DATA_FILE = "players_data.csv"
PHOTO_DIR = "photos"

# Create photo directory if not exists
os.makedirs(PHOTO_DIR, exist_ok=True)

# Load existing data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Name", "Village", "Category", "T-Shirt Size", "Mobile"])

# Initialize session state
if 'players' not in st.session_state:
    st.session_state.players = []

# Player registration form
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
            new_data = {
                "Name": name,
                "Village": village,
                "Category": category,
                "T-Shirt Size": tshirt_size,
                "Mobile": mobile
            }

            # Add to session for display
            st.session_state.players.append({
                **new_data,
                "Photo": photo.read() if photo else None
            })

            # Save to CSV
            df_new = pd.DataFrame([new_data])
            df = pd.concat([df, df_new], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            # Save photo if available
            if photo:
                image = Image.open(io.BytesIO(photo.read()))
                photo_path = os.path.join(PHOTO_DIR, f"{name}_{village}.jpg")
                image.save(photo_path)

            st.success(f"{name} registered successfully!")
        else:
            st.warning("Please fill all required fields!")

# Display registered players
st.header("Registered Players")

if not df.empty:
    for i, row in df.iterrows():
        st.markdown(f"*Name:* {row['Name']}")
        st.markdown(f"*Village:* {row['Village']}")
        st.markdown(f"*Category:* {row['Category']}")
        st.markdown(f"*T-Shirt Size:* {row['T-Shirt Size']}")
        st.markdown(f"*Mobile:* {row['Mobile']}")
        
        photo_path = os.path.join(PHOTO_DIR, f"{row['Name']}_{row['Village']}.jpg")
        if os.path.exists(photo_path):
            st.image(photo_path, width=120)
        st.markdown("---")

    # Download as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data as CSV", csv, "players.csv", "text/csv")

    # Download as Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Players')
    st.download_button("Download Data as Excel", output.getvalue(), "players.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.write("No players registered yet.")

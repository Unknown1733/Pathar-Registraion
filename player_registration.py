import streamlit as st
import pandas as pd
import base64
import io
import os
from PIL import Image

st.set_page_config(layout="centered", page_title="Pathar Premier League")

st.title("Pathar Tennis Ball Premier League - Player Registration")

ADMIN_SECRET = "patharadmin@2024"
CSV_FILE = "players_data.csv"

# Create CSV if it doesn't exist
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Name", "Village", "Category", "T-Shirt Size", "Mobile"])
    df_init.to_csv(CSV_FILE, index=False)

# --- PLAYER REGISTRATION FORM ---
with st.form("player_form"):
    st.subheader("Enter Player Details")
    name = st.text_input("Player Name")
    village = st.text_input("Village")
    category = st.selectbox("Category", ["All Rounder", "Batsman", "Bowler", "Wicket Keeper"])
    tshirt_size = st.text_input("T-Shirt Size")
    mobile = st.text_input("Mobile Number")
    photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Submit")

    if submitted:
        if name and village and mobile:
            # Save player data to CSV
            new_data = pd.DataFrame([{
                "Name": name,
                "Village": village,
                "Category": category,
                "T-Shirt Size": tshirt_size,
                "Mobile": mobile
            }])
            new_data.to_csv(CSV_FILE, mode='a', index=False, header=False)

            # Save photo if uploaded
            if photo:
                photo_dir = "player_photos"
                os.makedirs(photo_dir, exist_ok=True)
                with open(os.path.join(photo_dir, f"{name}_{mobile}.jpg"), "wb") as f:
                    f.write(photo.read())

            st.success("Registration successful! Thank you.")
            st.stop()
        else:
            st.warning("Please fill all required fields!")

# --- ADMIN PANEL TO VIEW & DOWNLOAD ALL DATA ---
st.divider()
admin_key = st.text_input("Admin Access Key", type="password", help="Only for organizer to download data.")

if admin_key == ADMIN_SECRET:
    st.success("Admin access granted.")

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)

        st.header("Registered Players")

        for i, row in df.iterrows():
            st.markdown(f"*Name:* {row['Name']}")
            st.markdown(f"*Village:* {row['Village']}")
            st.markdown(f"*Category:* {row['Category']}")
            st.markdown(f"*T-Shirt Size:* {row['T-Shirt Size']}")
            st.markdown(f"*Mobile:* {row['Mobile']}")
            image_path = f"player_photos/{row['Name']}_{row['Mobile']}.jpg"
            if os.path.exists(image_path):
                st.image(image_path, width=120)
            st.markdown("---")

        # CSV download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download All Data as CSV", csv, "players.csv", "text/csv")

        # Excel download
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Players')
        st.download_button("Download All Data as Excel", output.getvalue(), "players.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("No players registered yet.")
elif admin_key:
    st.error("Incorrect admin key.")

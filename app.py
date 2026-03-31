import streamlit as st
from PIL import Image
import gc
import os

st.set_page_config(page_title="Tire Auditor - Batch Mode", layout="wide")

st.title("✈️ Lion Air Asset Auditor (Batch Mode)")
st.info("Rename photos to the SN (e.g., 715FT132.jpg) before uploading.")

# Sidebar settings to reduce main page load
st.sidebar.header("Settings")
loc_choice = st.sidebar.radio("Location:", ["K177 (S/S Tire)", "K180 (U/S Tire)"])
loc_code = "K177" if "K177" in loc_choice else "K180"

# Step 1: Upload Files
files = st.file_uploader("Upload renamed photos", accept_multiple_files=True, type=['jpg','jpeg','png'])

if files:
    # Adding a 'Limit' slider helps prevent the browser from crashing 
    # while trying to show 300+ images at once
    view_limit = st.sidebar.slider("Photos to show per page:", 10, 100, 50)
    
    if st.button(f"🚀 Generate List (First {view_limit})"):
        # Process only the amount selected to save RAM
        for index, f in enumerate(files[:view_limit]):
            sn_from_file = os.path.splitext(f.name)[0].upper()
            wa_template = f"LOC: {loc_code}\nSN: {sn_from_file}\nREMARKS: UNRECORDED"
            
            c1, c2 = st.columns([1, 2])
            
            with c1:
                try:
                    img = Image.open(f)
                    # Force the image to be very small in memory
                    img.thumbnail((300, 300))
                    st.image(img, width=200)
                    del img
                except:
                    st.error(f"Error loading {f.name}")
            
            with c2:
                st.write(f"**Item {index+1}:** `{sn_from_file}`")
                st.code(wa_template, language="markdown")
            
            st.divider()
            gc.collect() # Clean memory after every single photo

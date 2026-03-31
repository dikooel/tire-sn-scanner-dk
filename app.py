import streamlit as st
from PIL import Image
import gc
import os

st.set_page_config(page_title="Tire Auditor - Filename Mode", layout="wide")

st.title("✈️ Lion Air Asset Auditor (Manual Mode)")
st.info("Rename your photos to the Serial Number (e.g., 715FT132.jpg) before uploading.")

# Step 1: Radio Button for Location
loc_choice = st.radio("Select Location:", ["K177 (S/S Tire)", "K180 (U/S Tire)"], horizontal=True)
loc_code = "K177" if "K177" in loc_choice else "K180"

# Step 2: Upload Files (Supports up to 400+ files easily now)
files = st.file_uploader("Upload renamed photos", accept_multiple_files=True, type=['jpg','jpeg','png'])

if files:
    if st.button("🚀 Generate List"):
        st.success(f"Processing {len(files)} files...")
        
        for index, f in enumerate(files):
            # Get the SN from the filename (e.g., "715FT132.jpg" -> "715FT132")
            sn_from_file = os.path.splitext(f.name)[0]
            
            # Format the WhatsApp template
            wa_template = f"LOC: {loc_code}\nSN: {sn_from_file}\nREMARKS: UNRECORDED"
            
            # Layout: Photo on left, Copy box on right
            c1, c2 = st.columns([1, 1])
            
            with c1:
                img = Image.open(f)
                # Show a smaller version to keep the page snappy
                img.thumbnail((500, 500))
                st.image(img, use_container_width=False, width=300)
                st.caption(f"Filename: {f.name}")
            
            with c2:
                st.write(f"**Serial Number:** `{sn_from_file}`")
                # Built-in copy button in the top-right of this box
                st.code(wa_template, language="markdown")
                st.info("👆 Click the copy icon above for WhatsApp.")
            
            # Clean up memory
            del img
            gc.collect()
            st.divider()

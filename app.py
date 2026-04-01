import streamlit as st
from PIL import Image
import gc
import os

st.set_page_config(page_title="Tire Auditor - Clear Mode", layout="wide")

st.title("✈️ Lion Air Asset Auditor (Big Image Mode)")
st.info("Rename photos to the SN (e.g., 715FT132.jpg). Upload ~20 photos at a time.")

# Step 1: Settings
st.sidebar.header("Settings")
loc_choice = st.sidebar.radio("Location:", ["K177 (S/S Tire)", "K180 (U/S Tire)"])
loc_code = "K177" if "K177" in loc_choice else "K180"

# Step 2: Upload Files (Manual mode)
files = st.file_uploader("Upload renamed photos", accept_multiple_files=True, type=['jpg','jpeg','png'])

if files:
    # Processing button to generate the list
    if st.button("🚀 Generate List"):
        st.divider()
        st.success(f"Processing {len(files)} items...")
        
        for index, f in enumerate(files):
            # Get the SN from the filename and make it uppercase
            sn_from_file = os.path.splitext(f.name)[0].upper()
            
            # Formatted WhatsApp template
            wa_template = f"LOC: {loc_code}\nSN: {sn_from_file}\nREMARKS: UNRECORDED"
            
            # Layout: Image on left, Template on right
            # Adjusted ratio to give the big image room (1, 1 means 50/50 split)
            c1, c2 = st.columns([1, 1])
            
            with c1:
                try:
                    img = Image.open(f)
                    # Use a large thumbnail (1500px) so the copy/paste quality is high
                    # Thumbnail only shrinks if the original is bigger, preserving quality
                    img.thumbnail((1500, 1500)) 
                    # use_container_width=True makes the photo fill its column space
                    st.image(img, use_container_width=True)
                    st.caption(f"Photo {index+1} ({f.name}) - Right-click -> Copy Image")
                    del img
                except:
                    st.error(f"Error loading {f.name}")
            
            with c2:
                # Vertical spacer to help align text with the top of the photo
                st.write("") 
                st.write(f"**Item:** `{sn_from_file}`")
                # Built-in copy icon in the top-right of this box
                st.code(wa_template, language="markdown")
                st.info("👆 Click the copy icon for WhatsApp.")
            
            st.divider()
            # Clean up memory, but less aggressively than the '350 files' version
            gc.collect()

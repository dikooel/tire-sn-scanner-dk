import streamlit as st
import easyocr
import re
from PIL import Image
import numpy as np
import gc

st.set_page_config(page_title="Tire Auditor", page_icon="✈️", layout="wide")

# This part stays the same - the AI brain
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = load_reader()

def extract_sn(image):
    image.thumbnail((1000, 1000)) 
    results = reader.readtext(np.array(image))
    pattern = r'[A-Z0-9]{3}FT[0-9]{3}'
    for (_, text, _) in results:
        clean = text.replace(" ", "").upper()
        match = re.search(pattern, clean)
        if match: return match.group()
    return "NOT FOUND"

st.title("🛞 Tire Serial Number Extractor")

loc_choice = st.radio("Select Location:", ["K177 (S/S Tire)", "K180 (U/S Tire)"], horizontal=True)
loc_code = "K177" if "K177" in loc_choice else "K180"

files = st.file_uploader("Upload tire photos", accept_multiple_files=True, type=['jpg','jpeg','png'])

if files:
    if st.button("🔍 Start Processing"):
        for index, f in enumerate(files):
            img = Image.open(f)
            sn = extract_sn(img)
            
            # This is your template
            wa_template = f"LOC: {loc_code}\nSN: {sn}\nREMARKS: UNRECORDED"
            
            c1, c2 = st.columns([1, 1])
            with c1: 
                st.image(img, use_container_width=True)
                st.caption(f"Photo {index+1} - Right-click to copy image")
            with c2: 
                st.write(f"**Detected SN: {sn}**")
                # Using st.code creates a box with a built-in copy button!
                st.code(wa_template, language="markdown")
                st.info("👆 Click the icon in the top-right of the box above to copy.")
            
            del img
            gc.collect() 
            st.divider()

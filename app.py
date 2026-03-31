import streamlit as st
import easyocr
import re
from PIL import Image, ImageOps, ImageFilter
import numpy as np
import gc

st.set_page_config(page_title="Tire Auditor Pro", page_icon="✈️", layout="wide")

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = load_reader()

def extract_sn(image):
    # 1. Pre-process: Convert to grayscale and sharpen to help with blur
    img = image.convert('L').filter(ImageFilter.SHARPEN)
    
    # 2. Try 4 rotations (0, 90, 180, 270 degrees)
    # This fixes the "orientation" issue!
    for angle in [0, 90, 180, 270]:
        test_img = img.rotate(angle, expand=True)
        results = reader.readtext(np.array(test_img))
        
        pattern = r'[A-Z0-9]{3}FT[0-9]{3}'
        for (_, text, _) in results:
            clean = text.replace(" ", "").upper()
            match = re.search(pattern, clean)
            if match:
                return match.group()
                
    return "NOT FOUND"

st.title("🛞 Tire Serial Number Extractor")

loc_choice = st.radio("Select Location:", ["K177 (S/S Tire)", "K180 (U/S Tire)"], horizontal=True)
loc_code = "K177" if "K177" in loc_choice else "K180"

files = st.file_uploader("Upload tire photos", accept_multiple_files=True, type=['jpg','jpeg','png'])

if files:
    if st.button("🔍 Start Processing"):
        for index, f in enumerate(files):
            img = Image.open(f)
            # Use the new smarter extraction
            sn = extract_sn(img)
            
            wa_template = f"LOC: {loc_code}\nSN: {sn}\nREMARKS: UNRECORDED"
            
            c1, c2 = st.columns([1, 1])
            with c1: 
                st.image(img, use_container_width=True)
                st.caption(f"Photo {index+1}")
            with c2: 
                st.write(f"**Detected SN: {sn}**")
                # If it still fails, the user can type it manually in the code block
                st.code(wa_template, language="markdown")
                if sn == "NOT FOUND":
                    st.warning("👀 Try taking a closer photo with the flash on!")
            
            del img
            gc.collect() 
            st.divider()

import streamlit as st
import easyocr
import re
from PIL import Image, ImageFilter
import numpy as np
import gc

st.set_page_config(page_title="Tire Auditor", layout="wide")

@st.cache_resource
def load_reader():
    # Only load English to save memory
    return easyocr.Reader(['en'], gpu=False)

reader = load_reader()

def get_sn_from_img(np_img):
    # Search for the 8-digit pattern
    results = reader.readtext(np_img, detail=0) # detail=0 uses less RAM
    pattern = r'[A-Z0-9]{3}FT[0-9]{3}'
    for text in results:
        clean = text.replace(" ", "").upper()
        match = re.search(pattern, clean)
        if match: return match.group()
    return None

def process_smart(image):
    # 1. Shrink the image significantly to save RAM
    image.thumbnail((800, 800))
    
    # 2. Try normal orientation first
    sn = get_sn_from_img(np.array(image))
    if sn: return sn
    
    # 3. If failed, try ONLY 90 degrees (most common sideways angle)
    # Rotating 4 times is usually what causes the 'Oh No' crash
    rotated = image.rotate(90, expand=True)
    sn = get_sn_from_img(np.array(rotated))
    
    return sn if sn else "NOT FOUND"

st.title("🛞 Tire Serial Extractor")

loc_choice = st.radio("Location:", ["K177 (S/S Tire)", "K180 (U/S Tire)"], horizontal=True)
loc_code = "K177" if "K177" in loc_choice else "K180"

files = st.file_uploader("Upload photos", accept_multiple_files=True)

if files:
    if st.button("🔍 Process"):
        for i, f in enumerate(files):
            img = Image.open(f)
            # Pre-process to Grayscale to save memory
            img = img.convert('L') 
            
            sn = process_smart(img)
            wa_template = f"LOC: {loc_code}\nSN: {sn}\nREMARKS: UNRECORDED"
            
            c1, c2 = st.columns([1, 1])
            with c1:
                st.image(img, width=250)
            with c2:
                st.write(f"**SN: {sn}**")
                st.code(wa_template, language="markdown")
            
            # Absolute memory cleanup
            del img
            gc.collect()
            st.divider()

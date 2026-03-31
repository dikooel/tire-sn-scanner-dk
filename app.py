import streamlit as st
import easyocr
import re
from PIL import Image
import numpy as np
import gc
from pyzbar.pyzbar import decode

st.set_page_config(page_title="Tire SN Extractor", layout="wide")

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = load_reader()

def extract_sn(image):
    # 1. Try Barcode & QR Code first (High Accuracy)
    detected_objects = decode(image)
    for obj in detected_objects:
        data = obj.data.decode('utf-8').strip()
        
        # If it's the QR code (multiple parts), split by spaces and find the SN
        if " " in data:
            parts = data.split()
            for p in parts:
                if re.search(r'[A-Z0-9]{3}FT[0-9]{3}', p):
                    return p
        
        # If it's just the barcode or a single-string QR
        match = re.search(r'[A-Z0-9]{3}FT[0-9]{3}', data.upper())
        if match: return match.group()

    # 2. Fallback to Text OCR if no codes are found
    image.thumbnail((800, 800))
    results = reader.readtext(np.array(image.convert('L')), detail=0)
    for text in results:
        clean = text.replace(" ", "").upper()
        match = re.search(r'[A-Z0-9]{3}FT[0-9]{3}', clean)
        if match: return match.group()
        
    return "NOT FOUND"

st.title("🛞 Tire Serial Number Extractor by andikazhr")
loc_choice = st.radio("Location:", ["K177 (S/S Tire)", "K180 (U/S Tire)"], horizontal=True)
loc_code = "K177" if "K177" in loc_choice else "K180"

files = st.file_uploader("Upload photos", accept_multiple_files=True)

if files:
    if st.button("🚀 Process Batch"):
        for i, f in enumerate(files):
            img = Image.open(f)
            sn = extract_sn(img)
            wa_template = f"LOC: {loc_code}\nSN: {sn}\nREMARKS: UNRECORDED"
            
            c1, c2 = st.columns([1, 1])
            with c1: st.image(img, width=250)
            with c2:
                st.write(f"**Detected SN: {sn}**")
                st.code(wa_template, language="markdown")
            
            del img
            gc.collect()
            st.divider()

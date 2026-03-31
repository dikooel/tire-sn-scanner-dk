import streamlit as st
import easyocr
import re
from PIL import Image
import numpy as np
from st_copy_button import st_copy_button

st.set_page_config(page_title="Tire Auditor", page_icon="✈️", layout="wide")

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

def extract_sn(image):
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
        for f in files:
            img = Image.open(f)
            sn = extract_sn(img)
            wa_template = f"LOC: {loc_code}\nSN: {sn}\nREMARKS: UNRECORDED"
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1: st.image(img, use_container_width=True)
            with c2: st.subheader(f"`{sn}`")
            with c3:
                st_copy_button(text=wa_template, label="📋 Copy WhatsApp Text")
                st.code(wa_template, language=None)
            st.divider()

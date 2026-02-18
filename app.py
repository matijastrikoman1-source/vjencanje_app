import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Popis Gostiju", layout="centered")
st.title("💍 Popis Gostiju za Vjenčanje")

# 1. PRVO USPOSTAVLJAMO VEZU
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. ONDA ČITAMO PODATKE
try:
    df = conn.read(worksheet="List 1", ttl=5)
except Exception as e:
    st.error(f"Pokušao sam otvoriti 'List 1', ali Google kaže: {e}")
    st.stop()

# --- Ostatak tvog koda za unos gostiju ide ispod ---
# Primjer forme za unos:
with st.form("forma_za_unos"):
    ime = st.text_input("Ime i prezime gosta")
    grupa = st.selectbox("Grupa", ["Mladoženja", "Mladenka"])
    potvrda = st.radio("Dolazi?", ["Na čekanju", "Da", "Ne"])
    gumb = st.form_submit_button("Spremi u bazu")

    if gumb and ime:
        novi_red = pd.DataFrame([{"Ime i Prezime": ime, "Grupa": grupa, "Potvrda": potvrda}])
        df = pd.concat([df, novi_red], ignore_index=True)
        conn.update(worksheet="List 1", data=df)
        st.success(f"Dodan/a {ime}!")
        st.rerun()

# Prikaz tablice na dnu
st.divider()
st.subheader("Trenutni popis:")
st.dataframe(df)

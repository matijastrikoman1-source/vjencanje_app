import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Popis Gostiju", layout="centered")
st.title("💍 Popis Gostiju za Vjenčanje")

# 1. USPOSTAVLJAMO VEZU
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. ČITAMO PODATKE
try:
    df = conn.read(worksheet="List 1", ttl=5)
except Exception as e:
    st.error(f"Pokušao sam otvoriti 'List 1', ali Google kaže: {e}")
    st.stop()

# --- FORMA ZA UNOS ---
with st.form("forma_za_unos"):
    ime = st.text_input("Ime i prezime gosta")
    
    col1, col2 = st.columns(2)
    with col1:
        odrasli = st.checkbox("Odrasli")
    with col2:
        djeca = st.checkbox("Djeca")
        
    potvrda = st.radio("Dolazi?", ["Na čekanju", "Da", "Ne"])
    napomena = st.text_area("Napomena (alergije, posebne želje...)")
    
    gumb = st.form_submit_button("Spremi u bazu")

    if gumb and ime:
        # Određujemo tip gosta za stupac 'Grupa' na temelju kvačica
        tip_gosta = ""
        if odrasli and djeca:
            tip_gosta = "Odrasli + Djeca"
        elif odrasli:
            tip_gosta = "Odrasli"
        elif djeca:
            tip_gosta = "Djeca"
        else:
            tip_gosta = "Nije definirano"

        # Kreiramo novi red
        novi_red = pd.DataFrame([{
            "Ime i Prezime": ime, 
            "Grupa": tip_gosta, 
            "Potvrda": potvrda, 
            "Napomena": napomena
        }])
        
        # Spajamo i šaljemo u Google Sheets
        df = pd.concat([df, novi_red], ignore_index=True)
        
        try:
            conn.update(worksheet="List 1", data=df)
            st.success(f"Dodan/a {ime} ({tip_gosta})!")
            st.rerun()
        except Exception as e:
            st.error(f"Greška pri spremanju: {e}")

# PRIKAZ TABLICE
st.divider()
st.subheader("Trenutni popis:")
st.dataframe(df, use_container_width=True)

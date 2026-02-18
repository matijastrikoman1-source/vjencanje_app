import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Postavke aplikacije
st.set_page_config(page_title="Naša Svadba", page_icon="💍")
st.title("Lista Uzvanika 🥂")

# 2. Povezivanje s Google Sheets (čita link iz .streamlit/secrets.toml)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl="0")
except Exception as e:
    st.error("Problem s povezivanjem! Provjeri .streamlit/secrets.toml")
    df = pd.DataFrame(columns=['Ime i Prezime', 'Grupa', 'Potvrda', 'Napomena'])

# 3. Forma za unos novih gostiju
with st.expander("➕ Dodaj novog gosta"):
    with st.form("forma"):
        ime = st.text_input("Ime i Prezime")
        grupa = st.selectbox("Tko je to?", ["Obitelj", "Prijatelji", "Kumovi"])
        potvrda = st.radio("Dolaze?", ["Na čekanju", "Da", "Ne"], horizontal=True)
        gumb = st.form_submit_button("Spremi u bazu")
       
        if gumb and ime:
            novi = pd.DataFrame([[ime, grupa, potvrda, ""]], columns=['Ime i Prezime', 'Grupa', 'Potvrda', 'Napomena'])
            df = pd.concat([df, novi], ignore_index=True)
            conn.update(data=df)
            st.success(f"Dodan/a {ime}!")
            st.rerun()

# 4. Prikaz trenutne liste
st.divider()
st.subheader("Trenutni popis:")
st.dataframe(df, use_container_width=True)


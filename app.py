import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Postavke aplikacije
st.set_page_config(page_title="Naša Svadba", page_icon="💍")
st.title("Lista Uzvanika 🥂")

# 2. Povezivanje s Google Sheets (čita link iz .streamlit/secrets.toml)
try:
    df = conn.read(worksheet="List 1", ttl=5)
    st.write("Uspješno povezano s tablicom!") # Ovo će nam potvrditi da radi
except Exception as e:
    st.error(f"Pokušao sam otvoriti 'List 1', ali Google kaže: {e}")
    st.stop()
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
            conn.update(worksheet="List 1", data=df)
            st.success(f"Dodan/a {ime}!")
            st.rerun()

# 4. Prikaz trenutne liste
st.divider()
st.subheader("Trenutni popis:")
st.dataframe(df, use_container_width=True)





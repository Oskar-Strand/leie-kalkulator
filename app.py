import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Leiepris 2025", page_icon="🏡")

# Load artifacts
ridge = joblib.load("ridge_model.pkl")
feature_cols = joblib.load("feature_columns.pkl")
area_growth = joblib.load("area_growth.pkl")
nat_growth = joblib.load("national_growth.pkl")
rom_per_område = joblib.load("rom_per_område.pkl")
m2_per_område_rom = joblib.load("m2_per_område_rom.pkl")
områder = sorted(rom_per_område.keys())

def kr(x): return f"{x:,.0f} kr".replace(",", " ")

st.title("Leiepris-kalkulator 2025")
område = st.selectbox("Område", områder)
rom = st.selectbox("Rom", rom_per_område.get(område, []))
m2 = st.selectbox("Størrelse (m²)", m2_per_område_rom.get((område, rom), []))

if st.button("Beregn leie"):
    row = pd.DataFrame([{"år": 2024, "rom": int(rom), "størrelse_m2": float(m2)}])
    for c in feature_cols:
        if c.startswith("Område_"):
            row[c] = 0
    col = f"Område_{område}"
    if col in feature_cols: row[col] = 1
    row = row.reindex(columns=feature_cols, fill_value=0)

    base_2024 = float(ridge.predict(row)[0]) 
    g = float(area_growth.get(område, nat_growth))
    price_2025 = base_2024 * (1 + g) 

    st.subheader(kr(price_2025) + " / mnd")

    st.caption(f"2024-estimat: {kr(base_2024)} × Vekst {g*100:.1f}% = 2025-estimat")
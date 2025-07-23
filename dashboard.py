import subprocess
import streamlit as st
import json
import pandas as pd
import time
import pytz
from datetime import datetime

st.set_page_config(layout="wide", page_title="Dashboard Phishing", page_icon="📧")

# 🟢 Pantalla tipo hacker estilo matrix (inicial)
st.markdown("""
<pre style='color: lime; font-weight: bold;'>
           🐾 CAMPAÑA PHISHING — MILEXX 🐾  
</pre>
""", unsafe_allow_html=True)
time.sleep(2)

# 📥 Cargar datos
try:
    with open("data/phishing_campaigns.json", "r") as f:
        data = json.load(f)
except Exception as e:
    st.error(f"Error al obtener datos: {e}")
    st.stop()

df = pd.DataFrame(data.get("campaigns", []))
ultima_actualizacion_utc = pd.to_datetime(data.get("last_updated", ""), errors="coerce")

# 🌎 Convertir fechas a horario Argentina
argentina = pytz.timezone("America/Argentina/Buenos_Aires")
ultima_actualizacion_arg = ultima_actualizacion_utc.tz_convert(argentina) if pd.notna(ultima_actualizacion_utc) else None

# 🧹 Asegurar columnas necesarias
for col in ["url", "domain", "ip", "country", "malicious", "type", "source", "timestamp"]:
    if col not in df.columns:
        df[col] = "Desconocido"

# 📆 Convertir y ajustar timestamps
df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce').dt.tz_convert(argentina)
df["timestamp_str"] = df["timestamp"].dt.strftime('%Y-%m-%d %H:%M:%S')

# 🔹 Filtros al estilo Kibana
st.markdown("## 🎛️ Filtros de Campañas")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    tipo_sel = st.multiselect("Tipo de campaña", df['type'].dropna().unique().tolist(), default=df['type'].unique())

with col2:
    pais_sel = st.multiselect("País", df['country'].dropna().unique().tolist(), default=df['country'].unique())

with col3:
    fuente_sel = st.multiselect("Fuente", df['source'].dropna().unique().tolist(), default=df['source'].unique())

with col4:
    dias = st.slider("Últimos X días", 1, 30, 7)

with col5:
    maliciosa_sel = st.multiselect("¿Es maliciosa?", df['malicious'].dropna().unique().tolist(), default=df['malicious'].unique())

# 🔎 Búsqueda libre
st.markdown("### 🔎 Búsqueda por texto")
texto_libre = st.text_input("Buscar en URL / Dominio / IP", "")

# 🔧 Aplicar filtros
df_filtro = df.copy()

def neutralizar_url(url):
    return url.replace("http", "hxxp").replace(".", "[.]")

def neutralizar_ip(ip):
    return ip.replace(".", "[.]") if isinstance(ip, str) else ip

df_filtro["url"] = df_filtro["url"].apply(neutralizar_url)
df_filtro["ip"] = df_filtro["ip"].apply(neutralizar_ip)

# Filtros principales
if tipo_sel:
    df_filtro = df_filtro[df_filtro["type"].isin(tipo_sel)]
if pais_sel:
    df_filtro = df_filtro[df_filtro["country"].isin(pais_sel)]
if fuente_sel:
    df_filtro = df_filtro[df_filtro["source"].isin(fuente_sel)]
if maliciosa_sel:
    df_filtro = df_filtro[df_filtro["malicious"].isin(maliciosa_sel)]

# Filtro por días
fecha_limite = datetime.now(argentina) - pd.Timedelta(days=dias)
df_filtro = df_filtro[df_filtro["timestamp"] >= fecha_limite]

# Filtro por texto libre
if texto_libre:
    df_filtro = df_filtro[
        df_filtro["url"].str.contains(texto_libre, case=False, na=False) |
        df_filtro["domain"].str.contains(texto_libre, case=False, na=False) |
        df_filtro["ip"].str.contains(texto_libre, case=False, na=False)
    ]

# 🧾 Métricas y título
st.title("📧 Campañas de Phishing Detectadas")
st.markdown(f"📊 Campañas totales filtradas: **{len(df_filtro)}**")
st.markdown(f"📆 Mostrando campañas de los últimos **{dias} días**")
if pd.notna(ultima_actualizacion_arg):
    st.markdown(f"🕒 Última actualización de OpenPhish: **{ultima_actualizacion_arg.strftime('%Y-%m-%d %H:%M:%S')} (Argentina)**")

# 📋 Tabla
st.subheader("📋 Detalle de campañas")
st.dataframe(df_filtro[["url", "domain", "ip", "country", "malicious", "type", "source", "timestamp_str"]])

# 🌍 Campañas por país
st.subheader("🌍 Campañas por país")
st.bar_chart(df_filtro["country"].value_counts().head(10))

# ⚠️ IPs maliciosas
st.subheader("⚠️ IPs maliciosas detectadas")
st.bar_chart(df_filtro["malicious"].value_counts())

# 📨 Campañas por tipo
st.subheader("📨 Campañas por tipo")
st.bar_chart(df_filtro["type"].value_counts())

# 💾 Botón para descargar CSV
st.subheader("📎 Descargar campañas filtradas")
csv = df_filtro.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Descargar CSV",
    data=csv,
    file_name=f"campanias_phishing_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
    mime='text/csv'
)

# 🔁 Botón para ejecutar geolocalización de IPs
st.subheader("📍 Enriquecer campañas con ubicación geográfica")
if st.button("🌐 Geolocalizar IPs"):
    with st.spinner("Buscando coordenadas para las IPs..."):
        resultado = subprocess.run(["python", "geolocalizar_ips.py"], capture_output=True, text=True)
        if resultado.returncode == 0:
            st.success("✅ Geolocalización completada con éxito.")
            st.text(resultado.stdout)
            st.info("🔁 Recargá el dashboard para ver los resultados actualizados.")
        else:
            st.error("❌ Ocurrió un error al ejecutar el script.")
            st.text(resultado.stderr)

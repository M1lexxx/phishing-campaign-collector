
<p align="center">
  <img src="https://github.com/M1lexxx/phishing-campaign-collector/raw/main/logo-milexx.jpeg" alt="Milexx Cybersecurity Lab" width="300"/>
</p>

# 📧 Phishing Campaign Collector – Milexxx Cybersecurity Lab

Este proyecto fue desarrollado como herramienta para la recolección y visualización de campañas de phishing en tiempo real, integrando fuentes como VirusTotal y AbuseIPDB. Brinda una interfaz sencilla e interactiva mediante **Streamlit**, ideal para analistas de amenazas y equipos de ciberseguridad.

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Streamlit**
- **Requests**
- **PyYAML**
- **python-dotenv** (opcional)
- APIs: [VirusTotal](https://www.virustotal.com/), [AbuseIPDB](https://www.abuseipdb.com/)

---

## 📁 Estructura del proyecto

```
📦 phishing-campaign-collector/
├── 📂 data/                # Archivos de datos recolectados
├── 📂 utils/               # Funciones auxiliares reutilizables
├── config.example.yaml    # Plantilla de configuración (sin claves)
├── dashboard.py           # Código principal del dashboard
├── geolocalizar_ips.py    # Script de geolocalización de IPs
├── main.py                # Ejecución principal
├── requirements.txt       # Dependencias del proyecto
├── start.ps1              # Script de inicio (PowerShell)
├── starts.bat             # Script de inicio (Windows .bat)
└── .gitignore             # Exclusiones para seguridad y limpieza
```

---

## 🔐 Seguridad

**No se incluyen claves reales.**  
Configuración sensible como claves API debe ir en un archivo `config.yaml` (no subido) con esta estructura:

```yaml
abuseipdb_api_key: "TU_API_KEY"
virustotal_api_key: "TU_API_KEY"
```

O también podés usar variables de entorno con un archivo `.env`.

---

## ▶️ Cómo usar

1. Cloná el repositorio:
```bash
git clone https://github.com/M1lexxx/phishing-campaign-collector.git
cd phishing-campaign-collector
```

2. Creá un entorno virtual (opcional):
```bash
python -m venv venv
.
env\Scripts ctivate  # Windows
# o
source venv/bin/activate  # Linux/mac
```

3. Instalá las dependencias:
```bash
pip install -r requirements.txt
```

4. Configurá tu `config.yaml` con las claves correspondientes.

5. Ejecutá el dashboard:
```bash
streamlit run dashboard.py
```

---

## 👤 Autor

**Milexxx – Cybersecurity Lab**  
🔎 Proyecto educativo y de investigación en amenazas digitales y respuesta ante phishing.

---

## 📄 Licencia

MIT License – libre uso con atribución.

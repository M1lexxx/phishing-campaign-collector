@echo off
cd /d "%~dp0"
call venv\Scripts\activate

echo 🐍 Entorno virtual activado...
echo 🔄 Ejecutando actualización de campañas...
python main.py

echo 🚀 Iniciando dashboard Streamlit...
streamlit run dashboard.py

pause

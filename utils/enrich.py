import socket
import requests
import yaml

# 🔑 Cargar claves desde config.yaml una sola vez
def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()
ABUSE_KEY = config.get("abuseipdb_api_key")
VT_KEY = config.get("virustotal_api_key")

# 🧠 Obtener IP desde dominio
def get_ip_from_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

# 🌍 Obtener país desde IP
def get_country_from_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if response.status_code == 200:
            return response.json().get("country", "Desconocido")
    except:
        pass
    return "Desconocido"

# 🔍 Verificar IP con VirusTotal
def check_ip_virustotal(ip):
    try:
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        headers = {"x-apikey": VT_KEY}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json().get("data", {})
            attributes = data.get("attributes", {})
            stats = attributes.get("last_analysis_stats", {})
            return "Sí (VT)" if stats.get("malicious", 0) > 0 else "No"
    except:
        pass
    return None

# 🛡️ Verificar IP con AbuseIPDB (con fallback a VirusTotal)
def is_ip_malicious(ip):
    try:
        url = "https://api.abuseipdb.com/api/v2/check"
        headers = {"Accept": "application/json", "Key": ABUSE_KEY}
        params = {"ipAddress": ip, "maxAgeInDays": "30"}
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json().get("data", {})
            score = data.get("abuseConfidenceScore", 0)
            return "Sí (AbuseIPDB)" if score >= 50 else "No"
    except:
        pass

    # Si AbuseIPDB falla, usar VirusTotal
    return check_ip_virustotal(ip) or "Desconocido"

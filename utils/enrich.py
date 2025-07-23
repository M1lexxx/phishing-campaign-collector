import socket
import requests
import yaml

# 🧠 Obtener IP desde dominio
def get_ip_from_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None

# 🌍 Obtener país desde IP
def get_country_from_ip(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("country", "Desconocido")
    except Exception:
        pass
    return "Desconocido"

# 🔑 Leer API Keys desde config.yaml
def load_api_key():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config.get("abuseipdb_api_key")

def load_virustotal_key():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config.get("virustotal_api_key")

# 🛡️ Consultar IP en VirusTotal si falla AbuseIPDB
def check_ip_virustotal(ip):
    try:
        api_key = load_virustotal_key()
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        headers = {
            "x-apikey": api_key
        }
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            stats = response.json()["data"]["attributes"]["last_analysis_stats"]
            return "Sí (VT)" if stats["malicious"] > 0 else "No"
    except Exception:
        pass
    return None

# 🔍 Verificar si una IP es maliciosa usando AbuseIPDB o VirusTotal
def is_ip_malicious(ip):
    try:
        api_key = load_api_key()
        url = "https://api.abuseipdb.com/api/v2/check"
        querystring = {"ipAddress": ip, "maxAgeInDays": "30"}
        headers = {"Accept": "application/json", "Key": api_key}
        response = requests.get(url, headers=headers, params=querystring, timeout=5)
        if response.status_code == 200:
            score = response.json()['data']['abuseConfidenceScore']
            return "Sí (AbuseIPDB)" if score >= 50 else "No"
    except:
        pass

    # Fallback a VirusTotal si falla AbuseIPDB
    vt_result = check_ip_virustotal(ip)
    return vt_result if vt_result else "Desconocido"

import json
import requests
import time

archivo = "data/phishing_campaigns.json"

with open(archivo, "r") as f:
    data = json.load(f)

campanias = data.get("campaigns", [])

def geolocalizar_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if response.status_code == 200:
            info = response.json()
            if info["status"] == "success":
                return info["lat"], info["lon"]
    except:
        pass
    return None, None

nuevas = 0
for c in campanias:
    ip = c.get("ip")
    if not ip or ip in ["Desconocido", ""]:
        continue
    if "latitude" not in c or "longitude" not in c or c["latitude"] in [None, ""] or c["longitude"] in [None, ""]:
        lat, lon = geolocalizar_ip(ip)
        if lat and lon:
            c["latitude"] = lat
            c["longitude"] = lon
            nuevas += 1
            print(f"✔️ {ip} => {lat}, {lon}")
        else:
            print(f"❌ No se pudo geolocalizar: {ip}")
        time.sleep(1.5)  # evitar bloqueo por rate limit

with open(archivo, "w") as f:
    json.dump(data, f, indent=2)

print(f"\n✅ {nuevas} campañas fueron enriquecidas con coordenadas.")

import os
import json
import socket
import requests
import time
import concurrent.futures
from datetime import datetime, timezone
from utils.sources.openphish import get_openphish_urls
from utils.parser import extract_domain, classify_url
from utils.enrich import get_ip_from_domain, get_country_from_ip, is_ip_malicious

# 🐾 Banner con pitbull completo (oreja corregida)
print("""
 ███╗   ███╗██╗██╗     ███████╗██╗  ██╗██╗  ██╗     //\\_/\\
 ████╗ ████║██║██║     ██╔════╝╚██╗██╔╝██║ ██╔╝    (     0\\___
 ██╔████╔██║██║██║     █████╗   ╚███╔╝ █████╔╝     /         O
 ██║╚██╔╝██║██║██║     ██╔══╝   ██╔██╗ ██╔═██╗    /   (_____/  
 ██║ ╚═╝ ██║██║███████╗███████╗██╔╝ ██╗██║  ██╗  /_____/ 
 ╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
                🐾 CAMPAÑA PHISHING 🐾    
""")

def process_url(url, total, i):
    print(f"[+] Procesando {i}/{total}", end="\r")

    domain = extract_domain(url)
    tipo = classify_url(url)
    ip = get_ip_from_domain(domain)
    country = get_country_from_ip(ip) if ip else "No resuelta"
    malicious = is_ip_malicious(ip) if ip else "Desconocido"

    return {
        "url": url,
        "domain": domain,
        "ip": ip,
        "country": country,
        "malicious": malicious,
        "type": tipo,
        "source": "OpenPhish",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def main():
    print("\n🛠️  Estamos actualizando las campañas... aguarde un momento.\n")
    start_time = time.time()

    urls = get_openphish_urls()
    total_urls = len(urls)

    campaigns = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(process_url, url, total_urls, i+1) for i, url in enumerate(urls)]
        for future in concurrent.futures.as_completed(futures):
            campaigns.append(future.result())

    os.makedirs("data", exist_ok=True)
    output = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "campaigns": campaigns
    }

    with open("data/phishing_campaigns.json", "w") as f:
        json.dump(output, f, indent=4)

    end_time = time.time()
    duration = round(end_time - start_time, 2)

    print(f"\n\n[+] Se guardaron {len(campaigns)} campañas enriquecidas.")
    print(f"⏱️  Tiempo total: {duration} segundos\n")

if __name__ == "__main__":
    main()

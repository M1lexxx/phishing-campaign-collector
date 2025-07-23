import requests

def get_openphish_urls():
    url = "https://openphish.com/feed.txt"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            urls = response.text.strip().split('\n')
            return urls
        else:
            print(f"[!] Error {response.status_code} al acceder a OpenPhish.")
    except Exception as e:
        print(f"[!] Excepción al obtener datos de OpenPhish: {e}")
    return []

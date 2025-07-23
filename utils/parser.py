from urllib.parse import urlparse

def classify_url(url):
    if "googledocs" in url or "drive.google" in url:
        return "Google Docs Fake"
    elif "outlook" in url or "microsoft" in url:
        return "Outlook / Microsoft Login"
    elif "paypal" in url:
        return "PayPal"
    else:
        return "Otro"

def extract_domain(url):
    parsed = urlparse(url)
    return parsed.netloc

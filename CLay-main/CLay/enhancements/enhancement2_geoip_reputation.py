# enhancement2_geoip_reputation.py
# Deepika - Enhancement 2 + 3: GeoIP + Threat Reputation Lookup + Email Alerts

import requests
import geoip2.database
import os
import datetime
from CLay.enhancements.enhancement3_email_alert import send_alert  # 💌 IMPORT EMAIL SENDER

GEOIP_DB_PATH = "GeoLite2-City.mmdb"

# ✅ AbuseIPDB API Key
ABUSEIPDB_API_KEY = "dc41059e9b84b32e4ebcab52cf213ece1296f201647ff262195494253107bf3809ad7af16220c125"

def get_geo_info(ip):
    try:
        reader = geoip2.database.Reader(GEOIP_DB_PATH)
        response = reader.city(ip)
        country = response.country.name
        city = response.city.name
        return f"{country}, {city}"
    except Exception as e:
        return "GeoIP lookup failed"

def check_ip_reputation(ip):
    if not ABUSEIPDB_API_KEY:
        return "No AbuseIPDB API key set"
    try:
        response = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            params={"ipAddress": ip},
            headers={"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"}
        )
        data = response.json()["data"]
        score = data["abuseConfidenceScore"]
        return f"Abuse Score: {score}/100"
    except Exception as e:
        return "Reputation check failed"

def log_attacker_enhanced(ip, user_agent):
    now = datetime.datetime.now()
    geo_info = get_geo_info(ip)
    reputation = check_ip_reputation(ip)

    log_msg = f"{now} | IP: {ip} ({geo_info}) | {reputation} | Bad User-Agent: {user_agent}\n"

    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/attackers.log", "a") as f:
            f.write(log_msg)

        # Send email alert but avoid printing to terminal to keep console clean.
        try:
            send_alert(ip, geo_info, reputation, user_agent)
        except Exception:
            # suppress email errors to avoid terminal output
            pass

    except Exception:
        # Fail silently to avoid terminal output; dashboard will read the log file.
        pass

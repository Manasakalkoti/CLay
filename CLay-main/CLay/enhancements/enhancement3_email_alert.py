# enhancement3_email_alert.py
# Deepika - Enhancement 3: Email Alerts for Attacks

import smtplib
from email.message import EmailMessage

# ✅ Your Gmail + App Password
GMAIL_USER = "shekarshekarp440@gmail.com"  # <-- 🔁 Replace with your Gmail
GMAIL_APP_PASSWORD = "roqv ofgq scsv xhgb"  # <-- 🔁 Replace with your App Password

def send_alert(ip, geo, score, user_agent):
    try:
        msg = EmailMessage()
        msg["Subject"] = "🚨 Alert: Malicious IP Detected"
        msg["From"] = GMAIL_USER
        msg["To"] = GMAIL_USER

        msg.set_content(f"""
🚨 ATTACK DETECTED 🚨

IP Address: {ip}
Location: {geo}
Reputation: {score}
User-Agent: {user_agent}
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
    except Exception:
        # suppress email errors to avoid terminal output
        pass

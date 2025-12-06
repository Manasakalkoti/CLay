# CLay – Cyber Attack Detection & Logging System

CLay is a lightweight cybersecurity monitoring tool that detects malicious web requests, enriches them with geolocation + threat-reputation data, sends real-time alerts, and provides a visual dashboard to analyze attacks.

This project simulates features of a mini Security Operations Center (SOC) tool.

---

## 🚀 Features

### **1. Malicious User-Agent Detection**
The system detects common attacker tools such as:
- sqlmap
- curl
- nikto
- acunetix
When detected, it logs the attacker’s IP and User-Agent.  
📄 Reference: Enhancement 1 :contentReference[oaicite:5]{index=5}

---

### **2. GeoIP + Threat Reputation Lookup**
When a bad User-Agent is found:
- IP geolocation is retrieved using **MaxMind GeoLite2**
- Threat score is fetched from **AbuseIPDB**
- Logs are enriched with country, city, and reputation score  
📄 Reference: Enhancement 2 :contentReference[oaicite:6]{index=6}

---

### **3. Email Alert System**
When a malicious request is detected, the system:
- Sends an email alert using Gmail SMTP  
- Includes IP, geolocation, reputation score, and User-Agent  
📄 Reference: Enhancement 3 :contentReference[oaicite:7]{index=7}

This brings real SOC-style alerting into the project.

---

### **4. Visual Dashboard**
A Flask-based dashboard:
- Reads from `logs/attackers.log`
- Displays attacks in a formatted table (time, IP, location, reputation, User-Agent)
- Highlights malicious entries
- Runs on **http://localhost:8080**  
📄 References: Enhancement 4 :contentReference[oaicite:8]{index=8} :contentReference[oaicite:9]{index=9}

---

## 📁 Project Structure




You must also download:
- GeoLite2 database  
- AbuseIPDB API key  
- Gmail App Password (for email alerts)

---

## ▶️ Running the System

### **1. Start the backend**
This will:
- Log attacker
- Enrich with GeoIP + reputation
- Send an email alert
- Display in dashboard

---

## 📬 Email Alert Example

Alerts include:
- IP Address  
- Geolocation  
- Threat score  
- User-Agent  

Sent automatically on detection.  
📄 Reference: Enhancement 3 :contentReference[oaicite:10]{index=10}

---

## 🧠 Learnings

- Handling attacker fingerprinting via User-Agents  
- Integrating GeoIP + reputation intelligence  
- Implementing secure email alerts  
- Building Flask dashboards with templates  
- Organizing logs and backend modules cleanly  

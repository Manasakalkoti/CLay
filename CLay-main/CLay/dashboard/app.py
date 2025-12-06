# app.py - Dashboard backend
from flask import Flask, render_template, jsonify
import os
import logging

app = Flask(__name__)

# Candidate log locations (search order):
# 1) Top-level project `logs/attackers.log`
# 2) Nested package `CLay-main/logs/attackers.log` (older layout)
# 3) Current working directory `logs/attackers.log`
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
CANDIDATE_LOGS = [
    os.path.join(PROJECT_ROOT, 'logs', 'attackers.log'),
    os.path.join(os.path.dirname(__file__), '..', 'logs', 'attackers.log'),
    os.path.join(os.getcwd(), 'logs', 'attackers.log')
]

def find_log_path():
    """Return the most recently modified existing log path from candidates.

    If none exist, return the first candidate as a fallback path.
    """
    existing = []
    for p in CANDIDATE_LOGS:
        p_abs = os.path.abspath(p)
        if os.path.exists(p_abs):
            try:
                mtime = os.path.getmtime(p_abs)
            except Exception:
                mtime = 0
            existing.append((mtime, p_abs))
    if existing:
        # pick the path with the newest modification time
        existing.sort(reverse=True)
        return existing[0][1]
    # fallback to first candidate
    return os.path.abspath(CANDIDATE_LOGS[0])


def parse_log_line(line):
    """Parse a log line into a dict. Returns None if parsing fails.

    Expected (enhanced) format:
      timestamp | IP: <ip> (<geo>) | <reputation> | Bad User-Agent: <ua>
    Falls back to simple formats when possible.
    """
    try:
        parts = [p.strip() for p in line.strip().split('|')]
        # If we have 4+ parts follow enhanced format
        if len(parts) >= 4:
            timestamp = parts[0]
            ip_info = parts[1]
            reputation = parts[2]
            user_agent = parts[3]

            ip = ip_info.split('(')[0].replace('IP:', '').strip()
            location = None
            if '(' in ip_info and ')' in ip_info:
                try:
                    location = ip_info.split('(', 1)[1].rsplit(')', 1)[0].strip()
                except Exception:
                    location = None

            return {
                'timestamp': timestamp,
                'ip': ip,
                'location': location,
                'reputation': reputation,
                'user_agent': user_agent
            }

        # If only 1 part, store raw line
        if len(parts) == 1:
            return {'raw': line.strip()}

    except Exception:
        return None


def read_logs():
    data = []
    log_path = find_log_path()
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as fh:
                for line in fh:
                    parsed = parse_log_line(line)
                    if parsed:
                        data.append(parsed)
        except Exception:
            pass
    return data


@app.route("/")
def dashboard():
    logs = read_logs()
    return render_template("dashboard.html", logs=logs)


@app.route('/logs')
def logs_api():
    """Return JSON list of parsed log entries for AJAX polling."""
    return jsonify(read_logs())


if __name__ == "__main__":
    # Reduce console noise: don't run Flask in debug mode and silence werkzeug access logs
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    app.run(debug=False, port=8080, use_reloader=False)

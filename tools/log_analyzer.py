import re
from collections import defaultdict, Counter

# Pattern to match: Date Time LEVEL Message
LOG_PATTERN = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '
    r'(?P<level>INFO|WARNING|ERROR) '
    r'(?P<message>.*)'
)

# Pattern to find failed logins
FAILED_LOGIN_PATTERN = re.compile(r'(?P<user>\S+) failed login from (?P<ip>\S+)')

def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if match:
        return match.groupdict()
    return None

def detect_suspicious_activity(entries):
    # Count failed logins per (User, IP) pair
    failures = defaultdict(int)
    for entry in entries:
        if entry["level"] == "WARNING":
            m = FAILED_LOGIN_PATTERN.search(entry["message"])
            if m:
                user_ip = (m.group("user"), m.group("ip"))
                failures[user_ip] += 1
    
    # Flag any with 3 or more failures
    suspicious = [ui for ui, count in failures.items() if count >= 3]
    return suspicious, failures

def main():
    log_file = "sample.log"
    print(f"--- Log Analyzer: Reading {log_file} ---")

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Could not find {log_file}. Make sure it is in the same folder.")
        return

    entries = []
    for line in lines:
        parsed = parse_log_line(line.strip())
        if parsed:
            entries.append(parsed)

    print(f"Total entries parsed: {len(entries)}\n")

    # 1. Count Log Levels
    levels = [e["level"] for e in entries]
    print("Log Level Summary:")
    for level, count in Counter(levels).items():
        print(f" - {level}: {count}")

    # 2. Detect Suspicious Activity (Brute Force)
    suspicious, all_failures = detect_suspicious_activity(entries)

    print("\nSecurity Check:")
    if suspicious:
        print("Potential Brute-Force Attacks Detected (3+ failed logins):")
        for user, ip in suspicious:
            print(f" - User: {user} | IP: {ip} | Failures: {all_failures[(user, ip)]}")
    else:
        print("No obvious brute-force patterns detected.")

    # 3. Show Errors
    errors = [e for e in entries if e["level"] == "ERROR"]
    if errors:
        print("\nCritical Errors:")
        for e in errors:
            print(f" - {e['timestamp']}: {e['message']}")

if __name__ == "__main__":
    main()
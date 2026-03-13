import requests
from bs4 import BeautifulSoup

# Patterns for common technologies
TECH_SIGNS = {
    "React": {"patterns": ["react", "react-dom"], "tag": "script"},
    "Vue.js": {"patterns": ["vue", "vue.min.js"], "tag": "script"},
    "jQuery": {"patterns": ["jquery"], "tag": "script"},
    "Bootstrap": {"patterns": ["bootstrap"], "tag": "link"},
    "WordPress": {"patterns": ["/wp-content/"], "tag": "link"},
    "Angular": {"patterns": ["angular", "ng-app"], "tag": "script"}
}

def detect_technologies(url: str):
    if not url.startswith(("http://", "https://")):
        print("Error: URL must start with http:// or https://")
        return set()

    print(f"Scanning {url}...")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching website: {e}")
        return set()

    soup = BeautifulSoup(response.text, "html.parser")
    detected = set()

    for tech_name, rule in TECH_SIGNS.items():
        target_tag = rule["tag"]
        patterns = rule["patterns"]

        for tag in soup.find_all(target_tag):
            tag_string = str(tag).lower()
            if any(p in tag_string for p in patterns):
                detected.add(tech_name)
                break
    
    return detected

def main():
    print("--- Web Technology Detector ---")
    url = input("Enter a website URL: ").strip()

    if not url:
        print("No URL provided.")
        return

    found = detect_technologies(url)

    print("\nScan Complete.")
    if found:
        print("Detected Technologies:")
        for tech in sorted(found):
            print(f" - {tech}")
    else:
        print("No known technologies detected.")

if __name__ == "__main__":
    main()
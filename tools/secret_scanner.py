import os
import re

# Simple patterns for common secrets
PATTERNS = [
    (r'sk-[a-zA-Z0-9]{20,}', "Possible OpenAI API Key"),
    (r'AKIA[0-9A-Z]{16}', "Possible AWS Access Key ID"),
    (r'(?i)password\s*=\s*["\'][^"\']{6,}["\']', "Possible Password Assignment"),
    (r'(?i)api[_-]?key\s*[:=]\s*["\'][^"\']{10,}["\']', "Possible API Key Assignment"),
]

def scan_file(filepath):
    findings = []
    try:
        with open(filepath, "r", errors="ignore") as f:
            for lineno, line in enumerate(f, start=1):
                for pattern, label in PATTERNS:
                    if re.search(pattern, line):
                        findings.append((lineno, line.strip(), label))
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return findings

def scan_folder(root_folder):
    all_findings = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            findings = scan_file(filepath)
            if findings:
                all_findings.append((filepath, findings))
    return all_findings

def main():
    target = "test_repo"
    
    if not os.path.isdir(target):
        print(f"Error: Folder '{target}' not found. Did you create it?")
        return

    print(f"--- Scanning folder: {target} ---\n")

    results = scan_folder(target)

    if not results:
        print("No potential secrets found.")
    else:
        print("Potential Secrets Found:")
        for filepath, findings in results:
            print(f"\nFile: {filepath}")
            for lineno, line, label in findings:
                print(f"  Line {lineno} [{label}]:")
                print(f"    {line}")

if __name__ == "__main__":
    main()
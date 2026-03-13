import re
import sys

def check_password_strength(password: str):
    """
    Analyzes a password string and returns a strength label and feedback list.
    """
    score = 0
    feedback = []

    # 1. Length Check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password is too short (use at least 8 characters).")

    # 2. Uppercase Check
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add uppercase letters (A-Z).")

    # 3. Lowercase Check
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add lowercase letters (a-z).")

    # 4. Digit Check
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Add digits (0-9).")

    # 5. Special Character Check
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Add special characters (!@#$%^&* etc.).")

    # Determine Strength Label
    if score >= 6:
        strength = "Strong"
    elif score >= 4:
        strength = "Medium"
    else:
        strength = "Weak"

    return strength, feedback

def main():
    print("--- Password Strength Checker ---")
    password = input("Enter a password to test: ").strip()
    
    if not password:
        print("No password entered.")
        return

    strength, feedback = check_password_strength(password)

    print(f"\nStrength: {strength}")
    if feedback:
        print("Suggestions to improve:")
        for item in feedback:
            print(f" - {item}")
    else:
        print("Great! Your password looks strong.")

if __name__ == "__main__":
    # Use try-except to handle closing the window gracefully
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
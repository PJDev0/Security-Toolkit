import bcrypt
from zxcvbn import zxcvbn


def hash_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(password, hashed_password):
    password_bytes = password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)


def check_strength(password):
    result = zxcvbn(password)
    score = result['score']
    
    strength_map = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Strong",
        4: "Very Strong"
    }
    
    return {
        'score': score,
        'strength': strength_map[score],
        'crack_time': result['crack_times_display']['offline_slow_hashing_1e4_per_second'],
        'warning': result['feedback']['warning'],
        'suggestions': result['feedback']['suggestions']
    }


def analyze_password(password):
    print(f"\n{'='*60}")
    print("PASSWORD ANALYSIS")
    print(f"{'='*60}")
    print(f"Password: {'*' * len(password)} ({len(password)} chars)")
    
    analysis = check_strength(password)
    print(f"\nStrength: {analysis['strength']}")
    print(f"Score: {analysis['score']}/4")
    print(f"Crack time: {analysis['crack_time']}")
    
    if analysis['warning']:
        print(f"\nWarning: {analysis['warning']}")
    
    if analysis['suggestions']:
        print("\nSuggestions:")
        for suggestion in analysis['suggestions']:
            print(f"  - {suggestion}")
    
    print(f"\n{'='*60}")
    print("BCRYPT HASH")
    print(f"{'='*60}")
    
    hashed = hash_password(password)
    print(f"Hash: {hashed}")
    
    print(f"\n{'='*60}")
    print("VERIFICATION")
    print(f"{'='*60}")
    print(f"Correct password: {'MATCH' if verify_password(password, hashed) else 'FAIL'}")
    print(f"Wrong password: {'MATCH' if verify_password('wrong', hashed) else 'NO MATCH'}")
    
    return hashed


def main():
    print("=" * 60)
    print("PASSWORD SECURITY DEMO")
    print("=" * 60)
    
    passwords = ["123456", "password", "Tr0ub4dor&3", "correcthorsebatterystaple"]
    
    for pwd in passwords:
        analyze_password(pwd)
        input("\nPress Enter to continue...")
        print()
    
    print("=" * 60)
    print("Demo complete.")


if __name__ == "__main__":
    main()
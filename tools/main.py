#!/usr/bin/env python3
import sys
import os

from hasher import hash_file, verify_file
from symmetric_crypto import generate_key, encrypt_message, decrypt_message, save_key, load_key
from asymmetric_crypto import (generate_rsa_keys, save_keys, load_private_key, 
                               load_public_key, encrypt_with_public_key, 
                               decrypt_with_private_key)
from password_security import hash_password, verify_password, check_strength


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print("=" * 70)
    print("PYTHON CRYPTOGRAPHY TOOLKIT v1.0")
    print("SHA-256 | AES-256 | RSA-2048 | bcrypt | zxcvbn")
    print("=" * 70)


def print_menu():
    print("\nMAIN MENU:")
    print("-" * 70)
    print("  [1] Hash a file (SHA-256)")
    print("  [2] Verify file integrity")
    print("  [3] Encrypt message (AES-256)")
    print("  [4] Decrypt message (AES-256)")
    print("  [5] Generate RSA key pair")
    print("  [6] Encrypt with RSA (public key)")
    print("  [7] Decrypt with RSA (private key)")
    print("  [8] Check password strength")
    print("  [9] Hash password (bcrypt)")
    print("  [10] Verify password")
    print("  [0] Exit")
    print("-" * 70)


def get_input(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\nGoodbye!")
        sys.exit(0)


def hash_file_menu():
    print("\n" + "=" * 60)
    print("SHA-256 FILE HASHING")
    print("=" * 60)
    
    filepath = get_input("Enter file path: ")
    if not os.path.exists(filepath):
        print("ERROR: File not found!")
        return
    
    file_hash = hash_file(filepath)
    if file_hash:
        print(f"\nFile: {os.path.abspath(filepath)}")
        print(f"SHA-256: {file_hash}")
        print(f"Length: {len(file_hash)}")
        
        if get_input("\nSave hash? (y/n): ").lower() == 'y':
            with open(filepath + ".sha256", "w") as f:
                f.write(file_hash)
            print("Hash saved.")


def verify_file_menu():
    print("\n" + "=" * 60)
    print("VERIFY FILE INTEGRITY")
    print("=" * 60)
    
    filepath = get_input("Enter file path: ")
    if not os.path.exists(filepath):
        print("ERROR: File not found!")
        return
    
    expected = get_input("Enter expected hash: ")
    is_valid, actual = verify_file(filepath, expected)
    
    print(f"\nExpected: {expected[:20]}...")
    print(f"Actual:   {actual[:20]}...")
    print(f"Result: {'VALID - File unchanged' if is_valid else 'INVALID - File modified'}")


def aes_encrypt_menu():
    print("\n" + "=" * 60)
    print("AES-256 ENCRYPTION")
    print("=" * 60)
    
    print("\nKey options:")
    print("  [1] Generate new key")
    print("  [2] Load existing key")
    print("  [3] Enter key (hex)")
    
    choice = get_input("Select: ")
    key = None
    
    if choice == "1":
        key = generate_key()
        print(f"Key: {key.hex()}")
        if get_input("Save? (y/n): ").lower() == 'y':
            save_key(key, "aes_key.key")
    elif choice == "2":
        key = load_key(get_input("Key file: "))
    elif choice == "3":
        key = bytes.fromhex(get_input("Enter 64 hex chars: "))
    else:
        print("Invalid option")
        return
    
    msg = get_input("Enter message: ")
    encrypted = encrypt_message(key, msg)
    print(f"\nEncrypted:\n{encrypted}")
    
    if get_input("\nSave? (y/n): ").lower() == 'y':
        with open(get_input("Filename: "), "w") as f:
            f.write(encrypted)
        print("Saved.")


def aes_decrypt_menu():
    print("\n" + "=" * 60)
    print("AES-256 DECRYPTION")
    print("=" * 60)
    
    key = bytes.fromhex(get_input("Enter key (64 hex): "))
    
    print("Input from:")
    print("  [1] Paste text")
    print("  [2] File")
    
    if get_input("Select: ") == "2":
        with open(get_input("File: "), "r") as f:
            encrypted = f.read()
    else:
        encrypted = get_input("Paste encrypted: ")
    
    result = decrypt_message(key, encrypted)
    print(f"\nResult: {result}")


def rsa_generate_menu():
    print("\n" + "=" * 60)
    print("RSA KEY GENERATION")
    print("=" * 60)
    
    private_key, public_key = generate_rsa_keys()
    password = get_input("Password for private key (Enter=none): ")
    save_keys(private_key, public_key, password or None)
    print("Keys generated. Keep private_key.pem SECRET!")


def rsa_encrypt_menu():
    print("\n" + "=" * 60)
    print("RSA ENCRYPTION")
    print("=" * 60)
    
    if not os.path.exists("public_key.pem"):
        print("ERROR: Generate keys first (option 5)")
        return
    
    public_key = load_public_key()
    msg = get_input("Enter message (max 200 chars): ")
    
    if len(msg) > 200:
        print("ERROR: Message too long")
        return
    
    encrypted = encrypt_with_public_key(public_key, msg)
    print(f"\nEncrypted:\n{encrypted}")


def rsa_decrypt_menu():
    print("\n" + "=" * 60)
    print("RSA DECRYPTION")
    print("=" * 60)
    
    if not os.path.exists("private_key.pem"):
        print("ERROR: private_key.pem not found")
        return
    
    password = get_input("Password (Enter=none): ") or None
    private_key = load_private_key(password=password)
    encrypted = get_input("Paste encrypted: ")
    
    result = decrypt_with_private_key(private_key, encrypted)
    print(f"\nDecrypted: {result}")


def password_strength_menu():
    print("\n" + "=" * 60)
    print("PASSWORD STRENGTH")
    print("=" * 60)
    
    password = get_input("Enter password: ")
    result = check_strength(password)
    
    print(f"\nStrength: {result['strength']}")
    print(f"Score: {result['score']}/4")
    print(f"Crack time: {result['crack_time']}")
    
    if result['warning']:
        print(f"Warning: {result['warning']}")
    if result['suggestions']:
        for s in result['suggestions']:
            print(f"  - {s}")


def password_hash_menu():
    print("\n" + "=" * 60)
    print("BCRYPT HASH")
    print("=" * 60)
    
    password = get_input("Enter password: ")
    hashed = hash_password(password)
    print(f"\nHash: {hashed}")
    print("Store this in database - never store plain passwords!")
    
    if get_input("\nSave? (y/n): ").lower() == 'y':
        with open("password_hash.txt", "w") as f:
            f.write(hashed)
        print("Saved.")


def password_verify_menu():
    print("\n" + "=" * 60)
    print("VERIFY PASSWORD")
    print("=" * 60)
    
    password = get_input("Enter password: ")
    hashed = get_input("Enter hash: ")
    
    if verify_password(password, hashed):
        print("\nMATCH")
    else:
        print("\nNO MATCH")


def main():
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = get_input("\nSelect: ")
        
        actions = {
            "1": hash_file_menu,
            "2": verify_file_menu,
            "3": aes_encrypt_menu,
            "4": aes_decrypt_menu,
            "5": rsa_generate_menu,
            "6": rsa_encrypt_menu,
            "7": rsa_decrypt_menu,
            "8": password_strength_menu,
            "9": password_hash_menu,
            "10": password_verify_menu,
            "0": lambda: sys.exit("\nGoodbye!"),
        }
        
        if choice in actions:
            try:
                actions[choice]()
            except Exception as e:
                print(f"ERROR: {e}")
        else:
            print("Invalid option")
        
        if choice != "0":
            input("\nPress Enter...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
        sys.exit(0)
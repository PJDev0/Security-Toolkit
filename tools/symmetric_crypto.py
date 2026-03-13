from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import os


def generate_key():
    return AESGCM.generate_key(bit_length=256)


def encrypt_message(key, plaintext):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    encrypted_package = base64.b64encode(nonce + ciphertext).decode('utf-8')
    return encrypted_package


def decrypt_message(key, encrypted_package):
    try:
        aesgcm = AESGCM(key)
        data = base64.b64decode(encrypted_package.encode('utf-8'))
        nonce = data[:12]
        ciphertext = data[12:]
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode('utf-8')
    except Exception as e:
        return f"ERROR: Decryption failed: {str(e)}"


def save_key(key, filename):
    with open(filename, "wb") as f:
        f.write(key)
    print(f"Key saved to: {filename}")
    print("WARNING: Keep this file secure!")


def load_key(filename):
    with open(filename, "rb") as f:
        return f.read()


def main():
    print("=" * 60)
    print("AES-256 SYMMETRIC ENCRYPTION DEMO")
    print("=" * 60)
    print("Same key encrypts and decrypts")
    
    print("\n[1] Generating AES-256 key...")
    key = generate_key()
    print(f"Key (hex): {key.hex()}")
    print(f"Key size: {len(key)} bytes")
    
    key_file = "aes_key.key"
    save_key(key, key_file)
    
    message = "This is a top secret message!"
    print(f"\n[2] Original: {message}")
    
    print("\n[3] Encrypting...")
    encrypted = encrypt_message(key, message)
    print(f"Encrypted: {encrypted[:60]}...")
    
    print("\n[4] Decrypting with SAME key...")
    decrypted = decrypt_message(key, encrypted)
    print(f"Decrypted: {decrypted}")
    
    print("\n[5] Testing with WRONG key...")
    wrong_key = generate_key()
    result = decrypt_message(wrong_key, encrypted)
    print(f"Result: {result}")
    
    if os.path.exists(key_file):
        os.remove(key_file)
        print("\nCleaned up key file.")
    
    print("\nDemo complete. Never lose your AES key!")


if __name__ == "__main__":
    main()
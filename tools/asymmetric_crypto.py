from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64
import os


def generate_rsa_keys():
    print("Generating 2048-bit RSA key pair...")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


def save_keys(private_key, public_key, password=None):
    if password:
        encryption = serialization.BestAvailableEncryption(password.encode())
        print("Private key protected with password")
    else:
        encryption = serialization.NoEncryption()
        print("WARNING: Private key saved without password")
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption
    )
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    with open("private_key.pem", "wb") as f:
        f.write(private_pem)
    with open("public_key.pem", "wb") as f:
        f.write(public_pem)
    
    print("Keys saved:")
    print("  private_key.pem (KEEP SECRET)")
    print("  public_key.pem (can be shared)")


def load_private_key(filepath="private_key.pem", password=None):
    with open(filepath, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=password.encode() if password else None
        )


def load_public_key(filepath="public_key.pem"):
    with open(filepath, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def encrypt_with_public_key(public_key, message):
    try:
        encrypted = public_key.encrypt(
            message.encode('utf-8'),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(), label=None)
        )
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        return f"ERROR: {str(e)}"


def decrypt_with_private_key(private_key, encrypted_message):
    try:
        encrypted = base64.b64decode(encrypted_message.encode('utf-8'))
        decrypted = private_key.decrypt(
            encrypted,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(), label=None)
        )
        return decrypted.decode('utf-8')
    except Exception as e:
        return f"ERROR: {str(e)}"


def main():
    print("=" * 60)
    print("RSA ASYMMETRIC ENCRYPTION DEMO")
    print("=" * 60)
    
    print("\n[1] Generating RSA key pair...")
    private_key, public_key = generate_rsa_keys()
    
    print("\n[2] Saving keys...")
    save_keys(private_key, public_key)
    
    print("\n[3] Encrypting with PUBLIC key...")
    message = "Meet at the secret location at midnight!"
    print(f"Message: {message}")
    encrypted = encrypt_with_public_key(public_key, message)
    print(f"Encrypted: {encrypted[:60]}...")
    
    print("\n[4] Decrypting with PRIVATE key...")
    decrypted = decrypt_with_private_key(private_key, encrypted)
    print(f"Decrypted: {decrypted}")
    
    print("\n[5] Security check:")
    print("    - Public key CANNOT decrypt")
    print("    - Without private key, data is lost forever")
    
    import time
    time.sleep(2)
    for f in ["private_key.pem", "public_key.pem"]:
        if os.path.exists(f):
            os.remove(f)
    print("\nCleaned up key files.")
    
    print("\nDemo complete!")


if __name__ == "__main__":
    main()
import hashlib
import os


def hash_file(filepath):
    if not os.path.exists(filepath):
        print("ERROR: File not found:", filepath)
        return None
    
    sha256_hash = hashlib.sha256()
    
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest()


def verify_file(filepath, expected_hash):
    actual_hash = hash_file(filepath)
    if actual_hash is None:
        return False, "File not found"
    return actual_hash.lower() == expected_hash.lower(), actual_hash


def hash_string(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def main():
    print("=" * 60)
    print("SHA-256 FILE HASHER")
    print("=" * 60)
    
    test_file = "test_document.txt"
    
    with open(test_file, "w") as f:
        f.write("This is a confidential document.\n")
        f.write("Do not distribute!")
    
    print(f"\nCreated test file: {test_file}")
    
    file_hash = hash_file(test_file)
    if file_hash:
        print(f"\nSHA-256 Hash: {file_hash}")
        print(f"Length: {len(file_hash)} characters")
        
        print("\nTesting integrity verification...")
        is_valid, _ = verify_file(test_file, file_hash)
        print(f"Original file: {'VALID' if is_valid else 'INVALID'}")
        
        print("\nModifying file...")
        with open(test_file, "a") as f:
            f.write(".")
        
        is_valid, new_hash = verify_file(test_file, file_hash)
        print(f"Modified file: {'VALID' if is_valid else 'INVALID'}")
        print(f"New hash: {new_hash}")
        print("Notice: One character change = completely different hash")
    
    if os.path.exists(test_file):
        os.remove(test_file)
        print("\nCleaned up test file.")


if __name__ == "__main__":
    main()
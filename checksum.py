import hashlib

def calculate_filehash(path_to_file): 
    sha256_hash = hashlib.sha256()
    with open(path_to_file,"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    checksum = sha256_hash.hexdigest()
    return checksum
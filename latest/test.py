import hashlib


def get_file_hashes(file_path):
    hash_algorithms = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]
    hashes = {}
    with open(file_path, "rb") as file:
        file_content = file.read()

        for algo in hash_algorithms:
            hash_object = hashlib.new(algo)
            hash_object.update(file_content)
            hashes[algo] = hash_object.hexdigest()

    return hashes


file_path = "tenlight.py"
hashes = get_file_hashes(file_path)

for algo, hash_value in hashes.items():
    print(f"{algo.upper()}: {hash_value}")

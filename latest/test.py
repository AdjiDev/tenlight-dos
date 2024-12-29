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

reference_hashes = {
    "md5": "a418a2d9e1ed066b4ec8fd61ab9fe08c",
    "sha1": "d8f3e6f16368cf05e2e825b0cb116bef9352ac6e",
    "sha224": "0395e450316a686ba2d7a7d3c38138e2562a1874185fe2391d0c7ad1",
    "sha256": "759c8740c902a801e63b16ca1d3df5d88622cd4c4245b8e35c3f531b513758c3",
    "sha384": "56517103f46cff934764da90359ca9bbede25775f11b13a0726b167eb165506c7c6063d3d7522600d5fb9b22a7628ec4",
    "sha512": "ad4e6cceaa7fa40f1d113bcc3c50bba3f79b0d7a76f448c6c741d4062c16b87a9799e5b760314b1cb353ffcfa493d71671065a2627f1ce92e21a2e969e5f2a67",
}

file_path = "tenlight.py"

hashes = get_file_hashes(file_path)

mismatch_found = False
for algo, hash_value in hashes.items():
    expected_hash = reference_hashes.get(algo)
    if expected_hash != hash_value:
        mismatch_found = True
        print(f"[MISMATCH] {algo.upper()} hash does not match!")
        print(f"Expected: {expected_hash}")
        print(f"Found:    {hash_value}")

if not mismatch_found:
    print("All file hashes match the reference hashes.")
else:
    print("One or more hashes do not match. Please update the file.")
    print("Potential backdoor detected! It is advisable to verify the integrity and source of this file.")

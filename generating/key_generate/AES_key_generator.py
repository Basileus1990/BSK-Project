from Crypto.Cipher import AES
from hashlib import sha256


# Generates 256-bit key from PIN
def hash_pin(pin: str):
    if not pin.isdigit():
        raise ValueError("PIN must be a digit")
    return sha256(pin.encode()).digest()


# Pin must be a 4-digit number
def aes_encrypt_file(file_to_encrypt: str, pin: str):
    key = hash_pin(pin)

    with open(file_to_encrypt, 'rb') as file:
        data = file.read()

    cipher = AES.new(key,AES.MODE_EAX)
    print(data)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    nonce = cipher.nonce

    '''
    len(nonce) = 16 bytes
    len(tag) = 16 bytes
    '''
    data = nonce + tag + ciphertext

    with open(file_to_encrypt, 'wb') as file:
        file.write(data)


def aes_decrypt_file(file_to_decrypt: str, pin: str):
    key = hash_pin(pin)




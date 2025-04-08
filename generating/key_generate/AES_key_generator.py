import os.path

from Crypto.Cipher import AES
from hashlib import sha256


##
# @brief Generates a 256-bit key from PIN code
#
# The function validates the given PIN code and generate a 256-bit code from given PIN code
#
# @param pin A PIN code as string
#
# @return The derived PIN code as a 256-bit key
def hash_pin(pin: str):
    if not pin.isdigit():
        raise ValueError("PIN must be a digit")
    return sha256(pin.encode()).digest()


##
# @brief Encrypts a file using a 4-digit PIN code and AES encryption
#
# The function reads a file from the given path, changes the given 4-digit PIN code to a 256-bit key, and then
# encrypt the file with this key using AES encryption.
#
# @param file_to_encrypt Path to the input file to encrypt
# @param pin 4-digit PIN code
#
# @return True if AES encryption was successful; False if the file was not found or encryption failed.
def aes_encrypt_file(file_to_encrypt: str, pin: str) -> bool:
    if not os.path.isfile(file_to_encrypt):
        return False
    try:
        key = hash_pin(pin)

        with open(file_to_encrypt, 'rb') as file:
            data = file.read()

        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        nonce = cipher.nonce
        '''
        len(nonce) = 16 bytes
        len(tag) = 16 bytes
        '''
        data = nonce + tag + ciphertext

        with open(file_to_encrypt, 'wb') as file:
            file.write(data)
        return True
    except Exception as e:
        print(e)
        return False


##
# @brief Decrypts a file using a 4-digit PIN code and AES decryption
#
# The function reads a file from the given path, changes the given 4-digit PIN code to a 256-bit key, and then
# decrypt the file with this key using AES decryption.
#
# @param file_to_encrypt Path to the input file to decrypt
# @param pin 4-digit PIN code
#
# @return Tuple (True,data) if AES decryption was successful, where 'data' is the decryption content;
#         Tuple (False, None) if the file was not found or decryption failed.
def aes_decrypt_file(file_to_decrypt: str, pin: str) -> (bool, bytes):
    if not os.path.isfile(file_to_decrypt):
        return False, None
    try:
        key = hash_pin(pin)

        with open(file_to_decrypt, 'rb') as file:
            encrypted_data = file.read()

        nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]

        decrypt_file = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = decrypt_file.decrypt_and_verify(ciphertext, tag)
        return True, data
    except Exception as e:
        print(e)
        return False, None

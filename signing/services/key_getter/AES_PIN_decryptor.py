## @file AES_PIN_decryptor.py
#  @brief Provides cryptographic utility functions for hashing and AES decryption.
#  @details This module contains functions to hash a PIN using SHA256 and to decrypt
#           data encrypted with AES in EAX mode.

from Crypto.Cipher import AES
from hashlib import sha256

## @brief Hashes a numeric PIN string using SHA256.
#  @param pin The numeric PIN string to hash.
#  @type pin str
#  @return The SHA256 hash of the PIN as bytes.
#  @rtype bytes
def hash_pin(pin: str) -> bytes:
    return sha256(pin.encode()).digest()


## @brief Decrypts data encrypted using AES in EAX mode.
#  @param encrypted_data The encrypted data, which includes a 16-byte nonce,
#                        a 16-byte tag, and the ciphertext.
#  @type encrypted_data bytes
#  @param pin The numeric PIN string used to derive the decryption key.
#  @type pin str
#  @return The decrypted data as bytes.
#  @rtype bytes
#  @exception ValueError If the `encrypted_data` is less than 32 bytes (too short to contain nonce and tag).
def aes_decrypt_file(encrypted_data: bytes, pin: str) -> bytes:
    if len(encrypted_data) < 32:
        raise ValueError
    key = hash_pin(pin)
    nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]

    decrypt_file = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = decrypt_file.decrypt_and_verify(ciphertext, tag)
    return data

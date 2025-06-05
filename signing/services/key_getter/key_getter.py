## @file key_getter.py
#  @brief Retrieves and decrypts a private key from a USB drive.
#  @details This module provides functionality to locate USB drives on Windows and Linux,
#           find a specific key file (`private_key.key`), read its encrypted content,
#           and decrypt it using a PIN to obtain an RSA private key. It defines
#           several custom exceptions to handle various error conditions during this process.

import os
import platform

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from .AES_PIN_decryptor import aes_decrypt_file

## @var WINDOWS_PLATFORM_NAME
#  @brief String constant representing the Windows platform identifier.
WINDOWS_PLATFORM_NAME = "Windows"

## @var LINUX_PLATFORM_NAME
#  @brief String constant representing the Linux platform identifier.
LINUX_PLATFORM_NAME = "Linux"

## @var KEY_FILE_NAME
#  @brief The expected filename of the encrypted private key on the USB drive.
KEY_FILE_NAME = "private_key.key"

# Platform-specific imports for USB drive detection
if platform.system() == WINDOWS_PLATFORM_NAME:
    from .usb_finder_windows import get_usb_mount_paths_windows
elif platform.system() == LINUX_PLATFORM_NAME:
    from .usb_finder_linux import get_usb_mount_paths_linux

## @brief Exception raised when the current operating system is not supported for USB key retrieval.
class UnsupportedPlatformException(Exception):
    pass

## @brief Exception raised when no USB drives are found connected to the system.
class NoUSBDrivesFoundException(Exception):
    pass

## @brief Exception raised when the key file is not found on any detected USB drives.
class NoKeyFoundException(Exception):
    pass

## @brief Exception raised when the key file is found on multiple USB drives, creating ambiguity.
class MultipleKeysFoundException(Exception):
    pass

## @brief Exception raised when the provided PIN is incorrect or the key file is corrupted/cannot be decrypted with the PIN.
class KeyOrPinInvalidException(Exception):
    pass

## @brief Exception raised when the decrypted key data cannot be parsed as a valid RSA private key.
class KeyInvalidException(Exception):
    pass


## @brief Retrieves and decrypts the RSA private key from a USB drive using a PIN.
#  @param pin The PIN code to decrypt the private key.
#  @type pin str
#  @return The decrypted RSA private key.
#  @rtype rsa.RSAPrivateKey
#  @exception UnsupportedPlatformException If the current operating system is not supported.
#  @exception NoUSBDrivesFoundException If no USB drives are detected.
#  @exception NoKeyFoundException If the key file is not found on any USB drive.
#  @exception MultipleKeysFoundException If the key file is found on more than one USB drive.
#  @exception KeyOrPinInvalidException If the PIN is incorrect or the key data is malformed leading to decryption failure.
#  @exception KeyInvalidException If the decrypted data cannot be loaded as a valid PEM-encoded private key.
def get_key(pin: str) -> rsa.RSAPrivateKey:
    if platform.system() == WINDOWS_PLATFORM_NAME:
        encrypted_key = _get_key_windows()
    elif platform.system() == LINUX_PLATFORM_NAME:
        encrypted_key = _get_key_linux()
    else:
        raise UnsupportedPlatformException()

    try:
        key = aes_decrypt_file(encrypted_key, pin)
    except Exception:
        raise KeyOrPinInvalidException()

    try:
        private_key = serialization.load_pem_private_key(
            key,
            password=None,
        )
    except Exception:
        raise KeyInvalidException()

    return private_key


## @brief Internal function to retrieve the encrypted key data from USB drives on Windows.
#  @details Calls `get_usb_mount_paths_windows` to find USB drives and then `_get_key_paths`
#           to locate and read the key file.
#  @return The encrypted key data as bytes.
#  @rtype bytes
#  @exception NoUSBDrivesFoundException If no USB drives are detected by `_get_key_paths`.
#  @exception NoKeyFoundException If the key file is not found on any detected USB drives by `_get_key_paths`.
#  @exception MultipleKeysFoundException If the key file is found on multiple USB drives by `_get_key_paths`.
#  @private
def _get_key_windows() -> bytes:
    usb_paths = get_usb_mount_paths_windows()
    return _get_key_paths(usb_paths)


## @brief Internal function to retrieve the encrypted key data from USB drives on Linux.
#  @details Calls `get_usb_mount_paths_linux` to find USB drives and then `_get_key_paths`
#           to locate and read the key file.
#  @return The encrypted key data as bytes.
#  @rtype bytes
#  @exception NoUSBDrivesFoundException If no USB drives are detected by `_get_key_paths`.
#  @exception NoKeyFoundException If the key file is not found on any detected USB drives by `_get_key_paths`.
#  @exception MultipleKeysFoundException If the key file is found on multiple USB drives by `_get_key_paths`.
#  @private
def _get_key_linux() -> bytes:
    usb_paths = get_usb_mount_paths_linux()
    return _get_key_paths(usb_paths)


## @brief Internal function to search for and read the key file from a list of USB paths.
#  @param usb_paths A list of file system paths where USB drives are mounted.
#  @type usb_paths list[str]
#  @return The content of the key file as bytes.
#  @rtype bytes
#  @exception NoUSBDrivesFoundException If the `usb_paths` list is empty.
#  @exception NoKeyFoundException If `KEY_FILE_NAME` is not found in any of the provided `usb_paths`.
#  @exception MultipleKeysFoundException If `KEY_FILE_NAME` is found in more than one path in `usb_paths`.
#  @private
def _get_key_paths(usb_paths: list[str]) -> bytes:
    if len(usb_paths) == 0:
        raise NoUSBDrivesFoundException()

    key = None
    for usb_path in usb_paths:
        if not os.path.exists(f"{usb_path}/{KEY_FILE_NAME}"):
            continue

        with open(f"{usb_path}/{KEY_FILE_NAME}", "rb") as key_file:
            tmp_key = key_file.read()
            if key is not None:
                raise MultipleKeysFoundException()
            key = tmp_key

    if key is None:
        raise NoKeyFoundException()

    return key
"""
The package responsible for getting the key from the USB drive
"""
import os
import platform

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from .AES_PIN_decryptor import aes_decrypt_file

WINDOWS_PLATFORM_NAME = "Windows"
LINUX_PLATFORM_NAME = "Linux"
KEY_FILE_NAME = "private_key.key"

if platform.system() == WINDOWS_PLATFORM_NAME:
    from .usb_finder_windows import get_usb_mount_paths_windows
elif platform.system() == LINUX_PLATFORM_NAME:
    from .usb_finder_linux import get_usb_mount_paths_linux

class UnsupportedPlatformException(Exception):
    pass

class NoUSBDrivesFoundException(Exception):
    pass

class NoKeyFoundException(Exception):
    pass

class MultipleKeysFoundException(Exception):
    pass

class KeyOrPinInvalidException(Exception):
    pass

class KeyInvalidException(Exception):
    pass


def get_key(pin: str) -> rsa.RSAPrivateKey:
    """
    Returns the key from the USB drive.

    Possible exceptions:

    - **NoUSBDrivesFoundException**
    - **NoKeyFoundException** -> When no key was found on any found devices.
    - **UnsupportedPlatformException**
    - **MultipleKeysFoundException** -> When the key file was found in multiple devices,
      so it is impossible to determine which is the correct one.
    """

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


def _get_key_windows() -> bytes:
    usb_paths = get_usb_mount_paths_windows()
    return _get_key_paths(usb_paths)


def _get_key_linux() -> bytes:
    usb_paths = get_usb_mount_paths_linux()
    return _get_key_paths(usb_paths)


def _get_key_paths(usb_paths) -> bytes:
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
"""
The package responsible for getting the key from the USB drive
"""
import os
import platform
from .usb_finder import get_usb_mount_paths_linux, get_usb_mount_paths_windows

WINDOWS_PLATFORM_NAME = "Windows"
LINUX_PLATFORM_NAME = "Linux"
KEY_FILE_NAME = "PDF-KEY.key"

class UnsupportedPlatformException(Exception):
    pass

class NoUSBDrivesFoundException(Exception):
    pass

class NoKeyFoundException(Exception):
    pass

class MultipleKeysFoundException(Exception):
    pass


def get_key() -> str:
    """
    Returns the key from the USB drive.

    Possible exceptions:

    - **NoUSBDrivesFoundException**
    - **NoKeyFoundException** -> When no key was found on any found devices.
    - **UnsupportedPlatformException**
    - **MultipleKeysFoundException** -> When the key file was found in multiple devices,
      so it is impossible to determine which is the correct one.
    """

    #TODO: Check if the key is in correct format (When we will have a generated key from the other application)
    if platform.system() == WINDOWS_PLATFORM_NAME:
        return _get_key_windows()
    elif platform.system() == LINUX_PLATFORM_NAME:
        return _get_key_linux()
    else:
        raise UnsupportedPlatformException()


def _get_key_windows() -> str:
    usb_paths = get_usb_mount_paths_windows()
    return get_key_paths(usb_paths)

def _get_key_linux() -> str:
    usb_paths = get_usb_mount_paths_linux()
    return get_key_paths(usb_paths)

def get_key_paths(usb_paths):
    if len(usb_paths) == 0:
        raise NoUSBDrivesFoundException()

    key = None
    for usb_path in usb_paths:
        if not os.path.exists(f"{usb_path}/{KEY_FILE_NAME}"):
            continue

        with open(f"{usb_path}/{KEY_FILE_NAME}", "r") as key_file:
            tmp_key = key_file.read()
            if key is not None:
                raise MultipleKeysFoundException()
            key = tmp_key

    if key is None:
        raise NoKeyFoundException()

    return key
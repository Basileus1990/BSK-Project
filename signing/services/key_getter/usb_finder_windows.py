"""
This file contains functions needed for usb path locations through get_usb_mount_paths.
"""

import wmi

def get_usb_mount_paths_windows() -> list[str]:
    """
        Convert device ID to the path
    """
    devices = get_usb_devices_windows()
    paths = [f'{driveID}' for driveID in devices]

    return paths


def get_usb_devices_windows() -> list[str]:
    """
        https://github.com/tjguk/wmi/blob/master/docs/cookbook.rst#find-drive-types

        Function to get device ID from remotable disk
    """
    c = wmi.WMI()
    devList=[]
    for device in c.Win32_LogicalDisk():
        if device.DriveType == 2:
            devList.append(device.DeviceID)
    return devList
## @file usb_finder_windows.py
#  @brief Provides functions to find USB drive letters on Windows systems.
#  @details This module uses the Windows Management Instrumentation (WMI) library
#           to identify removable disk drives (typically USB drives) and retrieve
#           their assigned drive letters.

import wmi


## @brief Retrieves the drive letters for all connected USB storage devices on a Windows system.
#  @details This function first calls `get_usb_devices_windows()` to get a list of DeviceIDs
#           (drive letters) for removable drives. It then formats these DeviceIDs
#           into a list of strings representing paths (e.g., "C:", "D:").
#  @return A list of strings, where each string is a drive letter followed by a colon
#          (e.g., ['E:', 'F:']) representing detected USB drives.
#          Returns an empty list if no removable drives are found.
#  @rtype list[str]
def get_usb_mount_paths_windows() -> list[str]:
    """
        Convert device ID to the path
    """
    devices = _get_usb_devices_windows()
    paths = [f'{driveID}' for driveID in devices]

    return paths


## @brief Identifies removable logical disks on a Windows system.
#  @details This function queries WMI for `Win32_LogicalDisk` instances and filters them
#           based on `DriveType == 2`, which indicates a removable disk.
#           It collects the `DeviceID` (drive letter, e.g., "E:") for each such disk.
#           Source: https://github.com/tjguk/wmi/blob/master/docs/cookbook.rst#find-drive-types
#  @return A list of strings, where each string is the DeviceID (drive letter) of a
#          removable disk (e.g., ['E:', 'F:']).
#  @rtype list[str]
#  @private
def _get_usb_devices_windows() -> list[str]:
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
## @file usb_finder_linux.py
#  @brief Provides functions to find USB device mount paths on Linux systems.
#  @details This module uses system utilities like `glob` and `lsblk` to identify
#           connected USB storage devices and determine their mount points.
#           The primary function `get_usb_mount_paths_linux` is intended for use
#           by other modules needing to access files on USB drives.

import os
import subprocess
from glob import glob


## @brief Identifies USB block devices connected to a Linux system.
#  @details This function filters `/sys/block` for entries corresponding to USB storage devices (typically `sd*`).
#           It checks the device path for the presence of "usb" to confirm it's a USB device.
#           Source: https://stackoverflow.com/a/64000192
#  @return A list of base names for USB block devices (e.g., ['sdb', 'sdc']).
#  @rtype list[str]
#  @private
def _get_usb_devices_linux() -> list[str]:
    # This line filters the /sys/block for usb (sd*) files
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
                   if any(['usb' in dev.split('/')[5],
                           'usb' in dev.split('/')[6]]))
    return [os.path.basename(dev) for dev in usb_devices]


## @brief Retrieves the mount paths for all connected USB storage devices on a Linux system.
#  @details This function first gets the list of USB block devices using `_get_usb_devices_linux`.
#           Then, for each device, it uses the `lsblk` command to find its mount point(s).
#           It parses the output of `lsblk` to extract and return a list of valid mount paths.
#           Source: https://stackoverflow.com/a/64000192
#  @return A list of strings, where each string is an absolute mount path of a USB device.
#          Returns an empty list if no USB devices are mounted or found.
#  @rtype list[str]
def get_usb_mount_paths_linux() -> list[str]:
    devices = _get_usb_devices_linux()
    devices_mounting_points = []
    for dev in devices:
        # This command returns all locations where the device is mounted
        devices_mounting_points.append(subprocess.check_output(['lsblk', '-lnpo', 'NAME,MOUNTPOINT', '/dev/' + dev]).splitlines())

    paths = []
    for mounting_points in devices_mounting_points:
        for mnt_point in mounting_points:
            mnt_point_split = mnt_point.split(b' ', 1)
            if len(mnt_point_split) > 1 and mnt_point_split[1].strip():
                paths.append(mnt_point_split[1].decode('utf-8'))
    return paths

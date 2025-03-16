"""
This file contains functions needed for usb path locations through get_usb_mount_paths.
"""

import os
import subprocess
from glob import glob


def _get_usb_devices_linux() -> list[str]:
    """
    Source: https://stackoverflow.com/a/64000192

    This function returns the list of USB devices connected to the system.
    """

    # This line filters the /sys/block for usb (sd*) files
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
                   if any(['usb' in dev.split('/')[5],
                           'usb' in dev.split('/')[6]]))
    return [os.path.basename(dev) for dev in usb_devices]

def get_usb_mount_paths_linux() -> list[str]:
    """
    Source: https://stackoverflow.com/a/64000192

    This function returns the list of usb mount paths connected to the system.
    """

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

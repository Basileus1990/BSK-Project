"""
This frame is the view for checking for usb drive and reading the key from it
"""

import tkinter as tk
from signing.services.key_getter import key_getter
from typing import Callable


class GetKeyFromUSBFrame(tk.Frame):
    def __init__(self, parent: tk.Tk, return_result: Callable[[str], None]):
        tk.Frame.__init__(self, parent)

        self.return_result = return_result

        self.label = tk.Label(
            self,
            text="To sign the pdf file first the key has to be read from the USB drive",
            font=("TkDefaultFont", 16),
            wraplength=750,
        )
        self.label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.button = tk.Button(
            self,
            text="Find and read the key",
            command=self.get_key,
            font=("TkDefaultFont", 16)
        )
        self.button.pack(side=tk.TOP, padx=5, pady=5)


    def get_key(self):
        try:
            key = key_getter.get_key()
        except key_getter.UnsupportedPlatformException:
            self.label['text'] = "Current platform is not supported"
            self.button['text'] = "Exit the program"
            self.button['command'] = lambda: exit(0)
            return

        except key_getter.NoUSBDrivesFoundException:
            self.label['text'] = "No USB drives found. Please insert the USB drive and try again"
            self.button['text'] = "Try Again"
            return

        except key_getter.NoKeyFoundException:
            self.label['text'] = "No key found. Please check again if the key file is present in the USB drive and try again"
            self.button['text'] = "Try Again"
            return

        except key_getter.MultipleKeysFoundException:
            self.label['text'] = "The key file is present on more than one USB drive. Please make sure, that only one USB drive with the key file is inserted and try again"
            self.button['text'] = "Try Again"
            return

        self.return_result(key)

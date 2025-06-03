"""
This frame is the view for checking for usb drive and reading the key from it
"""

import tkinter as tk

from cryptography.hazmat.primitives.asymmetric import rsa
from services import key_getter
from typing import Callable


class KeyFromUSBFrame(tk.Frame):
    def __init__(self, parent: tk.Tk, return_result: Callable[[rsa.RSAPrivateKey], None]):
        tk.Frame.__init__(self, parent)

        self.return_result = return_result

        self.label = tk.Label(
            self,
            text="To sign the pdf file first the key has to be read from the USB drive and deciphered with PIN number",
            font=("TkDefaultFont", 16),
            wraplength=750,
        )
        self.label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.label_pin = tk.Label(self, text="PIN:")
        self.label_pin.pack(anchor='center', padx=5)
        self.pin_entry = tk.Entry(self, width=10)
        self.pin_entry.pack(padx=5, pady=(0, 10), anchor="center")

        self.button = tk.Button(
            self,
            text="Find and read the key",
            command=self.get_key,
            font=("TkDefaultFont", 16)
        )
        self.button.pack(side=tk.TOP, padx=5, pady=5)


    def get_key(self):
        pin = self.pin_entry.get()
        if pin is None or len(pin) == 0:
            self.label['text'] = "PIN is required"
            self.button['text'] = "Try Again"
            return

        if len(pin) != 4 or not pin.isdigit():
            self.label['text'] = "The PIN must be 4 digits. Please try again"
            self.button['text'] = "Try Again"
            return


        try:
            key = key_getter.get_key(pin)
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

        except key_getter.KeyOrPinInvalidException:
            self.label['text'] = "Either key or pin is invalid. Please make sure they are correct and try again"
            self.button['text'] = "Try Again"
            return

        except key_getter.KeyOrPinInvalidException:
            self.label['text'] = "Key is invalid. Please make sure it is correct and try again"
            self.button['text'] = "Try Again"
            return

        self.return_result(key)

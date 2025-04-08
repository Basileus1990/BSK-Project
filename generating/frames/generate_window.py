'''
    This frame is the view for keys generator app
'''

import tkinter as tk
from tkinter import filedialog
from typing import Callable
from generating.key_generate.RSA_key_generator import generate_keys
from generating.key_generate.AES_key_generator import aes_encrypt_file, aes_decrypt_file

PRIVATE_KEY_NAME = "private_key.key"
PUBLIC_KEY_NAME = "public_key.key"


class GenerateKeys(tk.Frame):
    def __init__(self, parent: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(
            self,
            text="Generator",
            font=("TkDefaultFont", 16),
            wraplength=750,
        )
        self.label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # text area for entry keys uri
        self.label_public_key = tk.Label(self, text="Public Key localization:")
        self.label_public_key.pack(anchor='center', padx=5)
        self.public_key_localization = tk.Entry(self, width=50)
        self.public_key_localization.pack(padx=5, pady=(0, 10), anchor="center")

        self.label_private_key = tk.Label(self, text="Private Key localization:")
        self.label_private_key.pack(anchor='center', padx=5)
        self.private_key_localization = tk.Entry(self, width=50)
        self.private_key_localization.pack(padx=5, pady=(0, 10),anchor="center")

        self.button_explore_public = tk.Button(
            self,
            text="Set Public Key localization",
            command=lambda: self.folder(self.public_key_localization))

        self.button_explore_private = tk.Button(
            self,
            text="Set Private Key localization",
            command=lambda: self.folder(self.private_key_localization))

        self.button_generate = tk.Button(
            self,
            text="Generate keys",
            command=lambda: self.generate_keys(self.public_key_localization.get(), self.private_key_localization.get(),self.pin_entry.get()))

        self.label_pin = tk.Label(self, text="PIN:")
        self.label_pin.pack(anchor='center', padx=5)
        self.pin_entry = tk.Entry(self, width=10)
        self.pin_entry.pack(padx=5, pady=(0, 10), anchor="center")

        # self.button_decrypt = tk.Button(
        #     self,
        #     text="Decrypt",
        #     command=lambda: self.decrypt_private_key(self.private_key_entry.get()))

        self.button_generate.pack(padx=5,pady=5)
        # self.button_decrypt.pack(padx=5, pady=5)
        self.pin_entry.pack(padx=5,pady=5)
        self.button_explore_public.pack(side=tk.TOP, padx=5, pady=5)
        self.button_explore_private.pack(side=tk.TOP, padx=5, pady=5)

        self.result = tk.Label(self,text=".")
        self.result.pack(padx=5,pady=10)

    # Open file dialog for choosing folder
    def folder(self, entry):
        folder = filedialog.askdirectory(title="Select a public key")

        if folder:
            entry.delete(0, tk.END)
            entry.insert(0, folder)

    # generate a pair of keys in RSA
    def generate_keys(self, public_location: str, private_location: str, pin: str):
        if not pin.isdigit() or len(pin) != 4:
            self.result.configure(text="PIN code must be 4 digit")
            return

        # check if uri's are empty
        if not public_location or not private_location:
            self.result.configure(text="Choose destinations")
            return

        # add keys name to uri
        public_location += ("/" + PUBLIC_KEY_NAME)
        private_location += ("/" + PRIVATE_KEY_NAME)

        if generate_keys(public_location, private_location):
            self.result.configure(text="Done")
            if aes_encrypt_file(private_location, pin):
                self.result.configure(text="Done")
            else:
                self.result.configure(text="Failed")
        else:
            self.result.configure(text="Failed")

    #@TODO do usuniecia bo tylko 2 aplikacji do podpisywania
    def decrypt_private_key(self, private_location: str, pin: str):
        if not pin.isdigit() or len(pin) != 4:
            return

        if private_location:
            private_location += ("/" + PRIVATE_KEY_NAME)
            data = aes_decrypt_file(private_location, pin)
            if data[0]:
                self.result.configure(text="Done")
            else:
                self.result.configure(text="Failed")
        else:
            self.result.configure(text="Choose destinations")
'''
    This frame is the view for keys generator app
'''

import tkinter as tk
from tkinter import filedialog
from typing import Callable
from generating.key_generate.RSA_key_generator import generate_keys


PRIVATE_KEY_NAME = "private_key.key"
PUBLIC_KEY_NAME = "public_key.key"


class GenerateKeys(tk.Frame):
    def __init__(self, parent: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(
            self,
            text="Hello world",
            font=("TkDefaultFont", 16),
            wraplength=750,
        )
        self.label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # text area for entry keys uri
        self.public_key_entry = tk.Entry(self,width=50)
        self.private_key_entry = tk.Entry(self,width=50)

        self.button_explore_public = tk.Button(
            self,
            text="Public Key",
            command=lambda: self.folder(self.public_key_entry))

        self.button_explore_private = tk.Button(
            self,
            text="Private Key",
            command=lambda: self.folder(self.private_key_entry))

        self.button_generate = tk.Button(
            self,
            text="Generate",
            command=lambda: self.generate_keys(self.public_key_entry.get(), self.private_key_entry.get()))

        self.button_generate.pack(padx=5,pady=5)
        self.button_explore_public.pack(side=tk.TOP, padx=5, pady=5)
        self.button_explore_private.pack(side=tk.TOP, padx=5, pady=5)

        self.public_key_entry.pack(padx=5,pady=10)
        self.private_key_entry.pack(padx=5, pady=10)

        self.result = tk.Label(self,text=".")
        self.result.pack(padx=5,pady=10)

    # Open file dialog for choosing folder
    def folder(self, entry):
        folder = filedialog.askdirectory(title="Select a public key")

        if folder:
            entry.delete(0, tk.END)
            entry.insert(0, folder)

    # generate a pair of keys in RSA
    def generate_keys(self,public_location: str,private_location: str):
        # check if uri's are empty
        if public_location and private_location:
            # add keys name to uri
            public_location += ("/"+PUBLIC_KEY_NAME)
            private_location += ("/"+PRIVATE_KEY_NAME)
            if generate_keys(public_location, private_location):
                self.result.configure(text="Done")
            else:
                self.result.configure(text="Failed")
        else:
            self.result.configure(text="Choose destinations")



"""
This frame is the start view. From here it is possible to go to signing or verifying part of application
"""

import tkinter as tk
from typing import Callable


class StartFrame(tk.Frame):
    def __init__(self, parent: tk.Tk, signing_chosen: Callable[[], None], verifying_chosen: Callable[[], None]):
        tk.Frame.__init__(self, parent)

        self.signing_chosen = signing_chosen
        self.verifying_chosen = verifying_chosen

        self.label = tk.Label(
            self,
            text="Please choose whether you want to sign a PDF or verify the signature",
            font=("TkDefaultFont", 16),
            wraplength=750,
        )
        self.label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.sign_button = tk.Button(
            self,
            text="Sign a PDF file",
            command=lambda : self.signing_chosen(),
            font=("TkDefaultFont", 16)
        )
        self.sign_button.pack(side=tk.TOP, padx=5, pady=5)

        self.verify_button = tk.Button(
            self,
            text="Verify a PDF file",
            command=lambda : self.verifying_chosen(),
            font=("TkDefaultFont", 16)
        )
        self.verify_button.pack(side=tk.TOP, padx=5, pady=5)

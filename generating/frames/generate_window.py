##
# @file generate_window.py
# @brief GUI window for generating RSA key pairs
# @details Provides input fields for taking a path to saving public/private keys, setting 4-digit PIN and a progress bar to display the current status of the generating process.
#
import time
import tkinter as tk
import threading
from tkinter import filedialog, ttk
from generating.key_generate.RSA_key_generator import generate_keys
from generating.key_generate.AES_key_generator import aes_encrypt_file

## @var PRIVATE_KEY_NAME
#  @brief Default filename for the private key
PRIVATE_KEY_NAME = "private_key.key"

## @var PUBLIC_KEY_NAME
#  @brief Default filename for the public key
PUBLIC_KEY_NAME = "public_key.key"

FOREGROUND_COLOR = "#ffffff"
BACKGROUND_COLOR = "#1e1e1e"
BACKGROUND2_COLOR = "#2d2d2d"
BLUE_BUTTON_COLOR = "#007acc"
ACTIVATE_BUTTON_COLOR = "#005f99"

class GenerateKeys(tk.Frame):
    def __init__(self, parent: tk.Tk):
        tk.Frame.__init__(self, parent)

        self.configure(bg=BACKGROUND_COLOR, padx=20, pady=20)

        self.progress_bar_style = ttk.Style(self)
        self.progress_bar_style.theme_use("alt")
        self.progress_bar_style.configure("green.Horizontal.TProgressbar",
                             troughcolor="white",
                             background="green")

        self.progress_bar_style.configure("red.Horizontal.TProgressbar",
                             troughcolor="white",
                             background="red")

        self.show_header_label()
        self.show_path_field()
        self.show_generate_button()
        self.show_pin()
        self.show_progress_bar()

    def show_header_label(self):
        # Header label
        self.header_label = tk.Label(
            self,
            text="Key Generator",
            font=("TkDefaultFont", 16),
            fg=FOREGROUND_COLOR,
            bg=BACKGROUND_COLOR,
            wraplength=750
        )
        self.header_label.pack(pady=(0, 20))

    def show_path_field(self):
        # Header path selection
        self.path_label = tk.Label(
            self,
            text="Key Storage Locations",
            font=("TkDefaultFont", 16),
            fg=FOREGROUND_COLOR,
            bg=BACKGROUND_COLOR,
            wraplength=750
        )
        self.path_label.pack(pady=5)

        # Public key selection
        self.label_public_key = tk.Label(self, text="Public Key localization:", fg=FOREGROUND_COLOR,
                                         bg=BACKGROUND_COLOR)
        self.label_public_key.pack(anchor='center', padx=5)
        self.public_key_localization = tk.Entry(self, width=50, fg=FOREGROUND_COLOR, bg=BACKGROUND2_COLOR,
                                                insertbackground="white")
        self.public_key_localization.pack(padx=5, pady=(0, 5), anchor="center")

        # Public key button
        self.button_explore_public = tk.Button(
            self,
            text="Set Public Key localization",
            bg=BLUE_BUTTON_COLOR,
            fg="white",
            activebackground=ACTIVATE_BUTTON_COLOR,
            relief="flat",
            command=lambda: self.open_folder(self.public_key_localization)
        )
        self.button_explore_public.pack(padx=5, pady=(0, 15), anchor="center")

        # Private key selection
        self.label_private_key = tk.Label(self, text="Private Key localization:", fg=FOREGROUND_COLOR,
                                          bg=BACKGROUND_COLOR)
        self.label_private_key.pack(anchor='center', padx=5)
        self.private_key_localization = tk.Entry(self, width=50, fg=FOREGROUND_COLOR, bg=BACKGROUND2_COLOR,
                                                 insertbackground="white")
        self.private_key_localization.pack(padx=5, pady=(0, 5), anchor="center")

        # Private key button
        self.button_explore_private = tk.Button(
            self,
            text="Set Private Key localization",
            bg=BLUE_BUTTON_COLOR,
            fg="white",
            activebackground=ACTIVATE_BUTTON_COLOR,
            relief="flat",
            command=lambda: self.open_folder(self.private_key_localization)
        )
        self.button_explore_private.pack(padx=5, pady=(0, 5), anchor="center")

    def show_pin(self):
        self.label_pin = tk.Label(self, text="PIN:", fg=FOREGROUND_COLOR, bg=BACKGROUND_COLOR)
        self.label_pin.pack(anchor='center', padx=5)
        self.pin_entry = tk.Entry(self, width=10)
        self.pin_entry.pack(padx=5, pady=(0, 10), anchor="center")
        self.pin_entry.pack(padx=5, pady=5)

    def show_progress_bar(self):
        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate",style="green.Horizontal.TProgressbar")
        self.status_label = tk.Label(self, text="", fg=FOREGROUND_COLOR, bg=BACKGROUND_COLOR)
        self.status_label.pack(pady=(10, 5))
        self.status_label.configure(text="Status")
        self.progress["value"] = 0
        self.progress.pack(pady=(0, 10))

    def show_generate_button(self):
        # Generate keys button
        self.button_generate = tk.Button(
            self,
            text="Generate keys",
            bg=BLUE_BUTTON_COLOR,
            fg="white",
            activebackground=ACTIVATE_BUTTON_COLOR,
            relief="flat",
            command=lambda: self.generate_keys_manager(self.public_key_localization.get(),
                                                       self.private_key_localization.get(), self.pin_entry.get())
        )
        self.button_generate.pack(padx=5, pady=(0, 5), anchor="center")

    # Open file dialog for choosing folder
    def open_folder(self, entry):
        folder = filedialog.askdirectory(title="Select a public key")

        if folder:
            entry.delete(0, tk.END)
            entry.insert(0, folder)

    # generate a pair of keys in RSA
    def generate_keys_manager(self, public_path: str, private_path: str, pin: str):
        self.update_status("Started...", 0, "green.Horizontal.TProgressbar")
        if not pin.isdigit() or len(pin) != 4:
            self.update_status("ERROR: PIN code must be 4 digit", 100, "red.Horizontal.TProgressbar")
            return

        # check if paths are empty
        if not public_path or not private_path:
            self.update_status("ERROR: Choose destinations", 100, "red.Horizontal.TProgressbar")
            return

        # add keys name to path
        public_path += ("/" + PUBLIC_KEY_NAME)
        private_path += ("/" + PRIVATE_KEY_NAME)

        threading.Thread(target=self.generate_keys_thread, args=(public_path, private_path, pin)).start()

    def generate_keys_thread(self, public_path: str, private_path: str, pin: str):
        self.update_status("Generating RSA keys...", 25,"green.Horizontal.TProgressbar")
        time.sleep(0.1)

        generating_rsa_success = generate_keys(public_path, private_path)

        if generating_rsa_success:
            self.update_status("RSA keys generated.",50,"green.Horizontal.TProgressbar")
            time.sleep(1)
        else:
            self.update_status("RSA keys generated failed",0,"green.Horizontal.TProgressbar")
            return

        encrypted_aes_success = aes_encrypt_file(private_path, pin)
        self.update_status("AES encryption...", 75,"green.Horizontal.TProgressbar")
        time.sleep(1)

        if encrypted_aes_success:
            self.update_status("Private key encrypted by PIN", 100,"green.Horizontal.TProgressbar")
        else:
            self.update_status("Private key encryption failed", 100,"red.Horizontal.TProgressbar")

    def update_status(self, message: str, progress: int, style: str):
        def update():
            self.status_label.configure(text=message)
            self.progress["value"] = progress
            self.progress.configure(style=style)
            self.update_idletasks()
        self.after(0, update)
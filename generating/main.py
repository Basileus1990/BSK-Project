## @file main.py
#  @brief Entry point for the key generating application
#  @details Launches the key generation GUI settings (width, height, title)

import tkinter as tk
from key_generate.RSA_key_generator import generate_keys
from frames.generate_window import GenerateKeys

APP_WIDTH = 400
APP_HEIGHT = 440
APP_TITLE = 'Generate keys'

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Basic configuration
        self.title(APP_TITLE)
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}')
        self.resizable(False, False)

        self.current_frame = GenerateKeys(self)
        self.current_frame.pack(fill='both', expand=True)


if __name__ == "__main__":
    App().mainloop()
## @file main.py
#  @brief Entry point for the key generating application.
#  @details Launches the key generation GUI with preset width, height and windows title.

import tkinter as tk
from frames.generate_window import GenerateKeys

APP_WIDTH = 400
APP_HEIGHT = 440
APP_TITLE = 'Generate keys'

##
# @class App
# @brief Main application class for key generation GUI.
#
# This class inherits from `tk.Tk` and loads the main GUI frame responsible
# for generating RSA keys and encrypting them using a 4-digit PIN.
#
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
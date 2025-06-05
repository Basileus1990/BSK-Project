## @file main.py
#  @brief Entry point for the signing application
#  @details Launches the signing application GUI settings (width, height, title)

import tkinter as tk

from cryptography.hazmat.primitives.asymmetric import rsa
from frames import KeyFromUSBFrame, StartFrame, SigningFrame, VerifyingFrame

APP_WIDTH = 800
APP_HEIGHT = 600
APP_TITLE = 'TEST APP'

##
# @class App
# @brief Main application class for the signing GUI.
#
# This class inherits from `tk.Tk` and loads the main GUI frame responsible
# for signing PDF files and verify theirs authentication.
#
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Basic configuration
        self.title(APP_TITLE)
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}')
        self.resizable(False, False)

        self.current_frame = StartFrame(self, self.start_signing, self.start_verifying)
        self.current_frame.pack(fill='both', expand=True)


    def start_signing(self):
        self._change_frame(KeyFromUSBFrame(self, self.get_key_from_usb_result))


    def start_verifying(self):
        self._change_frame(VerifyingFrame(self, self.main_menu))


    def get_key_from_usb_result(self, key: rsa.RSAPrivateKey):
        self._change_frame(SigningFrame(self, key, self.main_menu))


    def main_menu(self):
        self._change_frame(StartFrame(self, self.start_signing, self.start_verifying))


    def _change_frame(self, frame: tk.Frame):
        self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill='both', expand=True)


if __name__ == "__main__":
    App().mainloop()

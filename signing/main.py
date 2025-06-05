## @file main.py
#  @brief Entry point for the signing application
#  @details Launches the signing application GUI settings (width, height, title)

import tkinter as tk

from cryptography.hazmat.primitives.asymmetric import rsa
from frames import KeyFromUSBFrame, StartFrame, SigningFrame, VerifyingFrame

## @var APP_WIDTH
#  @brief The width of the application window in pixels.
APP_WIDTH = 800

## @var APP_HEIGHT
#  @brief The height of the application window in pixels.
APP_HEIGHT = 600

## @var APP_TITLE
#  @brief The title of the application window.
APP_TITLE = 'Signer APP'

## @class App
#  @brief Main application class that inherits from tkinter.Tk.
#  @details This class is responsible for initializing the main window and managing frame transitions.
class App(tk.Tk):
    ## @brief Initializes the App class.
    #  @details Sets up the window title, geometry, and resizability.
    #           It also initializes and displays the starting frame.
    def __init__(self):
        super().__init__()

        # Basic configuration
        self.title(APP_TITLE)
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}')
        self.resizable(False, False)

        self.current_frame = StartFrame(self, self.start_signing, self.start_verifying)
        self.current_frame.pack(fill='both', expand=True)

    ## @brief Switches the current frame to the KeyFromUSBFrame.
    def start_signing(self):
        self._change_frame(KeyFromUSBFrame(self, self.get_key_from_usb_result))

    ## @brief Switches the current frame to the VerifyingFrame.
    def start_verifying(self):
        self._change_frame(VerifyingFrame(self, self.main_menu))

    ## @brief Handles the result of the USB key retrieval and switches to the SigningFrame.
    #  @param key The RSA private key retrieved from the USB device.
    #  @type key rsa.RSAPrivateKey
    def get_key_from_usb_result(self, key: rsa.RSAPrivateKey):
        self._change_frame(SigningFrame(self, key, self.main_menu))

    ## @brief Switches the current frame back to the StartFrame (main menu).
    def main_menu(self):
        self._change_frame(StartFrame(self, self.start_signing, self.start_verifying))

    ## @brief Internal method to change the currently displayed frame.
    #  @param frame The new tkinter.Frame to display.
    #  @type frame tk.Frame
    #  @details Destroys the current frame and packs the new frame into the window.
    def _change_frame(self, frame: tk.Frame):
        self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill='both', expand=True)


if __name__ == "__main__":
    App().mainloop()

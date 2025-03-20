import tkinter as tk
from key_generate.key_RSA_generate import generate_keys
from frames.generate_window import GenerateKeys

APP_WIDTH = 800
APP_HEIGHT = 600
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
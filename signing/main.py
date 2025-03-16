import tkinter as tk
from tkinter import ttk

from frames.pendrive_check import GetKeyFromPendriveFrame

APP_WIDTH = 800
APP_HEIGHT = 600
APP_TITLE = 'TEST APP'

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Basic configuration
        self.title(APP_TITLE)
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}')
        self.resizable(False, False)

        # Setting the style
        self.style = ttk.Style(self)
        self.style.theme_use("default")  # Other options: alt, default, classic

        # The container for keeping the frames
        # container = ttk.Frame(self)
        # container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        self.current_frame = GetKeyFromPendriveFrame(self, self.get_key_from_pendrive_result)
        self.current_frame.pack(fill='both', expand=True)

    def get_key_from_pendrive_result(self, key: str):
        # self.current_frame.destroy()
        # self.current_frame = GetKeyFromPendriveFrame(self, lambda test: print(test))
        # self.current_frame.pack(fill='both', expand=True)
        print(key)


if __name__ == "__main__":
    App().mainloop()

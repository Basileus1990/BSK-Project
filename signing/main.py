import tkinter as tk

from frames.usb_check import GetKeyFromUSBFrame

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

        self.current_frame = GetKeyFromUSBFrame(self, self.get_key_from_usb_result)
        self.current_frame.pack(fill='both', expand=True)

    def get_key_from_usb_result(self, key: str):
        # self.current_frame.destroy()
        # self.current_frame = GetKeyFromUSBFrame(self, lambda test: print(test))
        # self.current_frame.pack(fill='both', expand=True)
        print(key)


if __name__ == "__main__":
    App().mainloop()

import tkinter as tk
from tkinter import ttk

APP_WIDTH = 800
APP_HEIGHT = 600
APP_TITLE = 'TEST APP'

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        # Basic configuration
        self.title(APP_TITLE)
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}')
        self.resizable(False, False)

        # Setting the style
        self.style = ttk.Style(self)
        self.style.theme_use("default")  # Other options: alt, default, classic

        # Create and arrange widgets
        self.create_widgets()

    def create_widgets(self):
        # Create main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add widgets
        self.label = ttk.Label(main_frame, text="Welcome to My App!")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(main_frame, width=40)
        self.entry.pack(pady=5)

        # Button container
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        self.submit_button = ttk.Button(
            button_frame,
            text="Submit",
            command=self.on_submit
        )
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(
            button_frame,
            text="Clear",
            command=self.on_clear
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Text widget
        self.text_output = tk.Text(main_frame, height=15, width=60)
        self.text_output.pack(pady=10, fill=tk.BOTH, expand=True)

    def on_submit(self):
        input_text = self.entry.get()
        self.text_output.insert(tk.END, f"Submitted: {input_text}\n")
        self.entry.delete(0, tk.END)

    def on_clear(self):
        self.text_output.delete(1.0, tk.END)


if __name__ == "__main__":
    MainApplication().mainloop()

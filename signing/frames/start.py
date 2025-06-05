"""
A Tkinter Frame providing options to navigate to PDF signing or verification sections.
"""

import tkinter as tk
from typing import Callable

# Constants for UI elements
LARGE_FONT_CONFIG = ("TkDefaultFont", 16)
DEFAULT_WRAP_LENGTH = 750
DEFAULT_PADDING_X = 200
DEFAULT_PADDING_Y = 10
BUTTON_PADDING_Y = 20

LABEL_TEXT = "Please choose whether you want to sign a PDF or verify the signature of a PDF file."
SIGN_BUTTON_TEXT = "Sign a PDF file"
VERIFY_BUTTON_TEXT = "Verify PDF file signature"

FOREGROUND_COLOR = "#ffffff"
BACKGROUND_COLOR = "#1e1e1e"
BACKGROUND2_COLOR = "#2d2d2d"
BLUE_BUTTON_COLOR = "#007acc"
ACTIVATE_BUTTON_COLOR = "#005f99"

class StartFrame(tk.Frame):
    def __init__(self, parent: tk.Tk, on_signing_chosen_callback: Callable[[], None], on_verifying_chosen_callback: Callable[[], None]):
        super().__init__(parent)

        self.on_signing_chosen_callback = on_signing_chosen_callback
        self.on_verifying_chosen_callback = on_verifying_chosen_callback

        self._setup_ui()

    def _setup_ui(self):
        """Creates and arranges UI elements within the frame."""
        self.configure(bg=BACKGROUND_COLOR)

        instruction_label = tk.Label(
            self,
            text=LABEL_TEXT,
            font=LARGE_FONT_CONFIG,
            wraplength=DEFAULT_WRAP_LENGTH,
            fg=FOREGROUND_COLOR,
            bg=BACKGROUND_COLOR,
        )
        instruction_label.pack(
            side=tk.TOP,
            fill=tk.X,
            pady=(DEFAULT_PADDING_Y, BUTTON_PADDING_Y * 2)
        )

        sign_button = tk.Button(
            self,
            text=SIGN_BUTTON_TEXT,
            command=self.on_signing_chosen_callback,
            font=LARGE_FONT_CONFIG,
            bg=BLUE_BUTTON_COLOR,
            fg="white",
            activebackground=ACTIVATE_BUTTON_COLOR,
        )
        sign_button.pack(
            side=tk.TOP,
            padx=DEFAULT_PADDING_X,
            pady=BUTTON_PADDING_Y,
            fill=tk.X
        )

        verify_button = tk.Button(
            self,
            text=VERIFY_BUTTON_TEXT,
            command=self.on_verifying_chosen_callback,
            font=LARGE_FONT_CONFIG,
            bg=BLUE_BUTTON_COLOR,
            fg="white",
            activebackground=ACTIVATE_BUTTON_COLOR,
        )
        verify_button.pack(
            side=tk.TOP,
            padx=DEFAULT_PADDING_X,
            pady=BUTTON_PADDING_Y,
            fill=tk.X
        )
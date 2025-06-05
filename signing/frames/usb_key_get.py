"""
A Tkinter Frame for prompting the user for a PIN to read and decrypt a private key from a USB drive.
"""

import tkinter as tk
from typing import Callable

from cryptography.hazmat.primitives.asymmetric import rsa
from services import key_getter

# Constants for UI elements and messages
LARGE_FONT_CONFIG = ("TkDefaultFont", 16)
DEFAULT_WRAP_LENGTH = 750
DEFAULT_PADDING_X = 10
DEFAULT_PADDING_Y = 10
INPUT_AREA_PADDING_Y = 5
BUTTON_PADDING_Y = 20

# Text constants
INITIAL_INSTRUCTION_TEXT = "To sign the PDF file, first the key has to be read from the USB drive and deciphered with your PIN."
PIN_LABEL_TEXT = "Enter PIN:"
ACTION_BUTTON_INITIAL_TEXT = "Find and Read Key"
ACTION_BUTTON_RETRY_TEXT = "Try Again"
ACTION_BUTTON_EXIT_TEXT = "Exit Program"

# Error/Status Messages
PIN_REQUIRED_MSG = "PIN is required. Please enter your 4-digit PIN."
PIN_INVALID_FORMAT_MSG = "The PIN must be 4 digits. Please try again."
UNSUPPORTED_PLATFORM_MSG = "Error: Current operating system is not supported for USB key retrieval."
NO_USB_DRIVES_MSG = "No USB drives found. Please insert the USB drive with the key and try again."
NO_KEY_FILE_MSG = "No key file found on any USB drive. Please ensure the key file is present and try again."
MULTIPLE_KEYS_MSG = "Multiple key files found across different USB drives. Please ensure only one USB drive with the key file is connected and try again."
KEY_OR_PIN_INVALID_MSG = "Invalid PIN or key file. Please verify your PIN and the key file, then try again."
KEY_INVALID_MSG = "The key file is invalid or corrupted. Please ensure you have the correct key file."

class KeyFromUSBFrame(tk.Frame):
    def __init__(self, parent: tk.Tk, on_key_retrieved_callback: Callable[[rsa.RSAPrivateKey], None]):
        super().__init__(parent)

        self.on_key_retrieved_callback = on_key_retrieved_callback
        self._setup_ui()

    def _setup_ui(self):
        """Creates and arranges UI elements within the frame."""
        self.status_label = tk.Label(
            self,
            text=INITIAL_INSTRUCTION_TEXT,
            font=LARGE_FONT_CONFIG,
            wraplength=DEFAULT_WRAP_LENGTH,
        )
        self.status_label.pack(side=tk.TOP, fill=tk.X, padx=DEFAULT_PADDING_X, pady=(DEFAULT_PADDING_Y, BUTTON_PADDING_Y))

        pin_label = tk.Label(self, text=PIN_LABEL_TEXT, font=("TkDefaultFont", 12))
        pin_label.pack(anchor='center', padx=DEFAULT_PADDING_X, pady=(INPUT_AREA_PADDING_Y, 0))

        self.pin_entry = tk.Entry(self, width=10, font=("TkDefaultFont", 14), justify='center', show='*')
        self.pin_entry.pack(padx=DEFAULT_PADDING_X, pady=(0, INPUT_AREA_PADDING_Y * 2), anchor="center")
        self.pin_entry.focus_set()

        self.action_button = tk.Button(
            self,
            text=ACTION_BUTTON_INITIAL_TEXT,
            command=self._process_pin_and_get_key,
            font=LARGE_FONT_CONFIG
        )
        self.action_button.pack(side=tk.TOP, padx=DEFAULT_PADDING_X, pady=BUTTON_PADDING_Y)

    def _update_feedback(self, status_message: str, button_text: str, button_command: Callable = None):
        """Helper to update status label and action button."""
        self.status_label.config(text=status_message)
        if button_command is None:
            button_command = self._process_pin_and_get_key
        self.action_button.config(text=button_text, command=button_command)
        self.pin_entry.delete(0, tk.END)

    def _process_pin_and_get_key(self):
        """Validates PIN and attempts to retrieve the key from USB."""
        pin = self.pin_entry.get()

        if not pin:
            self._update_feedback(PIN_REQUIRED_MSG, ACTION_BUTTON_RETRY_TEXT)
            return

        if len(pin) != 4 or not pin.isdigit():
            self._update_feedback(PIN_INVALID_FORMAT_MSG, ACTION_BUTTON_RETRY_TEXT)
            return

        try:
            private_key = key_getter.get_key(pin)
            self.on_key_retrieved_callback(private_key)

        except key_getter.UnsupportedPlatformException:
            self._update_feedback(UNSUPPORTED_PLATFORM_MSG, ACTION_BUTTON_EXIT_TEXT, lambda : exit(0))
        except key_getter.NoUSBDrivesFoundException:
            self._update_feedback(NO_USB_DRIVES_MSG, ACTION_BUTTON_RETRY_TEXT)
        except key_getter.NoKeyFoundException:
            self._update_feedback(NO_KEY_FILE_MSG, ACTION_BUTTON_RETRY_TEXT)
        except key_getter.MultipleKeysFoundException:
            self._update_feedback(MULTIPLE_KEYS_MSG, ACTION_BUTTON_RETRY_TEXT)
        except key_getter.KeyOrPinInvalidException: # Handles both invalid PIN and potentially invalid key issues
            self._update_feedback(KEY_OR_PIN_INVALID_MSG, ACTION_BUTTON_RETRY_TEXT)
        except key_getter.KeyInvalidException:
            self._update_feedback(KEY_INVALID_MSG, ACTION_BUTTON_RETRY_TEXT)
        except Exception as e:
            self._update_feedback(f"An error occurred: {type(e).__name__}. Please try again", ACTION_BUTTON_RETRY_TEXT)

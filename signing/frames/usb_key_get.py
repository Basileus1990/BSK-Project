## @file usb_key_get.py
#  @brief A Tkinter Frame for prompting the user for a PIN to read and decrypt a private key from a USB drive.
#  @details This frame handles user input for a PIN, interacts with the `key_getter` service
#           to retrieve an RSA private key from a USB device, and provides feedback to the user
#           regarding the success or failure of this operation.

import tkinter as tk
from typing import Callable

from cryptography.hazmat.primitives.asymmetric import rsa
from services import key_getter

## @var LARGE_FONT_CONFIG
#  @brief Font configuration for large text elements.
LARGE_FONT_CONFIG = ("TkDefaultFont", 16)

## @var DEFAULT_WRAP_LENGTH
#  @brief Default wrap length in pixels for text in labels.
DEFAULT_WRAP_LENGTH = 750

## @var DEFAULT_PADDING_X
#  @brief Default horizontal padding in pixels for UI elements.
DEFAULT_PADDING_X = 10

## @var DEFAULT_PADDING_Y
#  @brief Default vertical padding in pixels for general UI elements.
DEFAULT_PADDING_Y = 10

## @var INPUT_AREA_PADDING_Y
#  @brief Vertical padding in pixels for the PIN input area.
INPUT_AREA_PADDING_Y = 5

## @var BUTTON_PADDING_Y
#  @brief Specific vertical padding in pixels for buttons.
BUTTON_PADDING_Y = 20

## @var INITIAL_INSTRUCTION_TEXT
#  @brief Initial instruction text displayed to the user.
INITIAL_INSTRUCTION_TEXT = "To sign the PDF file, first the key has to be read from the USB drive and deciphered with your PIN."

## @var PIN_LABEL_TEXT
#  @brief Text for the PIN entry label.
PIN_LABEL_TEXT = "Enter PIN:"

## @var ACTION_BUTTON_INITIAL_TEXT
#  @brief Initial text for the main action button.
ACTION_BUTTON_INITIAL_TEXT = "Find and Read Key"

## @var ACTION_BUTTON_RETRY_TEXT
#  @brief Text for the action button when a retry is suggested.
ACTION_BUTTON_RETRY_TEXT = "Try Again"

## @var ACTION_BUTTON_EXIT_TEXT
#  @brief Text for the action button when exiting is the only option.
ACTION_BUTTON_EXIT_TEXT = "Exit Program"

## @var PIN_REQUIRED_MSG
#  @brief Error message when the PIN is not entered.
PIN_REQUIRED_MSG = "PIN is required. Please enter your 4-digit PIN."

## @var PIN_INVALID_FORMAT_MSG
#  @brief Error message when the PIN format is incorrect.
PIN_INVALID_FORMAT_MSG = "The PIN must be 4 digits. Please try again."

## @var UNSUPPORTED_PLATFORM_MSG
#  @brief Error message for unsupported operating systems.
UNSUPPORTED_PLATFORM_MSG = "Error: Current operating system is not supported for USB key retrieval."

## @var NO_USB_DRIVES_MSG
#  @brief Error message when no USB drives are detected.
NO_USB_DRIVES_MSG = "No USB drives found. Please insert the USB drive with the key and try again."

## @var NO_KEY_FILE_MSG
#  @brief Error message when the key file is not found on USB drives.
NO_KEY_FILE_MSG = "No key file found on any USB drive. Please ensure the key file is present and try again."

## @var MULTIPLE_KEYS_MSG
#  @brief Error message when multiple key files are found.
MULTIPLE_KEYS_MSG = "Multiple key files found across different USB drives. Please ensure only one USB drive with the key file is connected and try again."

## @var KEY_OR_PIN_INVALID_MSG
#  @brief Error message for an invalid PIN or key file.
KEY_OR_PIN_INVALID_MSG = "Invalid PIN or key file. Please verify your PIN and the key file, then try again."

## @var KEY_INVALID_MSG
#  @brief Error message when the key file itself is invalid or corrupted.
KEY_INVALID_MSG = "The key file is invalid or corrupted. Please ensure you have the correct key file."

FOREGROUND_COLOR = "#ffffff"
BACKGROUND_COLOR = "#1e1e1e"
BACKGROUND2_COLOR = "#2d2d2d"
BLUE_BUTTON_COLOR = "#007acc"
ACTIVATE_BUTTON_COLOR = "#005f99"


## @class KeyFromUSBFrame
#  @brief The KeyFromUSBFrame class handles the UI for retrieving a private key from a USB drive.
#  @details This frame prompts the user for a PIN, attempts to read and decrypt the key,
#           and then calls a callback function with the retrieved key or displays error messages.
#           It inherits from tk.Frame.
class KeyFromUSBFrame(tk.Frame):
    ## @brief Initializes the KeyFromUSBFrame.
    #  @param parent The parent tk.Tk window or tk.Frame that this frame will be placed in.
    #  @type parent tk.Tk
    #  @param on_key_retrieved_callback A function to be called when the private key is successfully retrieved.
    #                                    This callback should take one argument, the rsa.RSAPrivateKey, and return None.
    #  @type on_key_retrieved_callback Callable[[rsa.RSAPrivateKey], None]
    def __init__(self, parent: tk.Tk, on_key_retrieved_callback: Callable[[rsa.RSAPrivateKey], None]):
        super().__init__(parent)

        self.on_key_retrieved_callback = on_key_retrieved_callback
        self._setup_ui()

    ## @brief Sets up the user interface elements for the KeyFromUSBFrame.
    #  @details This private method creates and arranges the instruction label, PIN entry field,
    #           and action button within the frame.
    def _setup_ui(self):
        """Creates and arranges UI elements within the frame."""
        self.configure(bg=BACKGROUND_COLOR)

        self.status_label = tk.Label(
            self,
            text=INITIAL_INSTRUCTION_TEXT,
            font=LARGE_FONT_CONFIG,
            wraplength=DEFAULT_WRAP_LENGTH,
            fg=FOREGROUND_COLOR,
            bg=BACKGROUND_COLOR,
        )
        self.status_label.pack(side=tk.TOP, fill=tk.X, padx=DEFAULT_PADDING_X, pady=(DEFAULT_PADDING_Y, BUTTON_PADDING_Y))

        pin_label = tk.Label(self, text=PIN_LABEL_TEXT, font=("TkDefaultFont", 12),fg=FOREGROUND_COLOR,bg=BACKGROUND_COLOR)
        pin_label.pack(anchor='center', padx=DEFAULT_PADDING_X, pady=(INPUT_AREA_PADDING_Y, 0))

        self.pin_entry = tk.Entry(self, width=10, font=("TkDefaultFont", 14), justify='center', show='*', fg=FOREGROUND_COLOR, bg=BACKGROUND2_COLOR, insertbackground="white")
        self.pin_entry.pack(padx=DEFAULT_PADDING_X, pady=(0, INPUT_AREA_PADDING_Y * 2), anchor="center")
        self.pin_entry.focus_set()

        self.action_button = tk.Button(
            self,
            text=ACTION_BUTTON_INITIAL_TEXT,
            command=self._process_pin_and_get_key,
            font=LARGE_FONT_CONFIG,
            bg=BLUE_BUTTON_COLOR,
            fg="white",
            activebackground=ACTIVATE_BUTTON_COLOR,
        )
        self.action_button.pack(side=tk.TOP, padx=DEFAULT_PADDING_X, pady=BUTTON_PADDING_Y)

    ## @brief Updates the status label and action button with new messages and commands.
    #  @param status_message The message to display in the status label.
    #  @type status_message str
    #  @param button_text The new text for the action button.
    #  @type button_text str
    #  @param button_command The new command to associate with the action button. Defaults to _process_pin_and_get_key.
    #  @type button_command Callable
    #  @details This is a helper method to centralize UI updates for feedback.
    def _update_feedback(self, status_message: str, button_text: str, button_command: Callable = None):
        self.status_label.config(text=status_message)
        if button_command is None:
            button_command = self._process_pin_and_get_key
        self.action_button.config(text=button_text, command=button_command)
        self.pin_entry.delete(0, tk.END)

    ## @brief Processes the entered PIN and attempts to retrieve the private key from a USB drive.
    #  @details This method is called when the action button is pressed.
    #           It validates the PIN format, then calls the `key_getter.get_key` service.
    #           Based on the outcome, it either calls the `on_key_retrieved_callback` with the key
    #           or updates the UI with an appropriate error message using `_update_feedback`.
    #           It handles various exceptions that can be raised during the key retrieval process.
    def _process_pin_and_get_key(self):
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

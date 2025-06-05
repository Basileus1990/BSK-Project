## @file verifying.py
#  @brief A Tkinter Frame for selecting a PDF file and a public key to verify the PDF's digital signature.
#  @details This frame allows the user to select a PDF document and a public key file
#           to verify the integrity and authenticity of the PDF's digital signature.
#           It interacts with the `pdf_signer` service for the verification logic.

import tkinter as tk
from tkinter import filedialog
from typing import Callable

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pyhanko.pdf_utils.misc import PdfReadError
from services import pdf_signer


## @var LARGE_FONT_CONFIG
#  @brief Font configuration for large text elements like status labels and buttons.
LARGE_FONT_CONFIG = ("TkDefaultFont", 16)

## @var DEFAULT_WRAP_LENGTH
#  @brief Default wrap length in pixels for text in labels to ensure proper UI layout.
DEFAULT_WRAP_LENGTH = 750

## @var PDF_FILE_TYPES
#  @brief File type filter for PDF file selection dialogs, showing only "*.pdf" files.
PDF_FILE_TYPES = [("PDF files", "*.pdf")]

## @var PUBLIC_KEY_FILE_TYPES
#  @brief File type filter for public key file selection dialogs, showing "*.pem" and "*.key" files.
PUBLIC_KEY_FILE_TYPES = [("Public Key files", "*.pem *.key")]

## @var SELECT_PDF_TO_VERIFY_TITLE
#  @brief Title for the file dialog when selecting the PDF file to be verified.
SELECT_PDF_TO_VERIFY_TITLE = "Select the PDF file to verify"

## @var SELECT_PUBLIC_KEY_TITLE
#  @brief Title for the file dialog when selecting the public key file.
SELECT_PUBLIC_KEY_TITLE = "Select the public key file"

## @var DEFAULT_PADDING_X
#  @brief Default horizontal padding in pixels for UI elements.
DEFAULT_PADDING_X = 10

## @var DEFAULT_PADDING_Y
#  @brief Default vertical padding in pixels for general UI elements.
DEFAULT_PADDING_Y = 10

## @var SECTION_SPACING_Y
#  @brief Vertical spacing in pixels used between UI sections (e.g., between PDF selection and public key selection).
SECTION_SPACING_Y = 20

## @var BUTTON_PADDING_Y
#  @brief Specific vertical padding in pixels for buttons.
BUTTON_PADDING_Y = 20

## @var INITIAL_INSTRUCTION_TEXT
#  @brief Initial instructional text displayed to the user in the status label.
INITIAL_INSTRUCTION_TEXT = "Please choose the PDF file to verify and the public key corresponding to the signature."

## @var VERIFY_BUTTON_INITIAL_TEXT
#  @brief Initial text for the button that initiates the PDF signature verification process.
VERIFY_BUTTON_INITIAL_TEXT = "Verify PDF Signature"

## @var VERIFY_BUTTON_RETRY_TEXT
#  @brief Text for the main action button when a retry is suggested after an error.
VERIFY_BUTTON_RETRY_TEXT = "Try Again"

## @var VERIFY_BUTTON_GO_BACK_TEXT
#  @brief Text for the main action button to navigate back to the main menu after verification (success or failure).
VERIFY_BUTTON_GO_BACK_TEXT = "Go back to main menu"

## @var PATHS_REQUIRED_MSG
#  @brief Error message displayed if either the PDF file or public key file path is not selected.
PATHS_REQUIRED_MSG = "Both PDF file and public key file locations are required. Please select them."

## @var PUBLIC_KEY_NOT_FOUND_MSG
#  @brief Error message displayed if the specified public key file cannot be found.
PUBLIC_KEY_NOT_FOUND_MSG = "Public key file not found at the specified location. Please check the path and try again."

## @var PUBLIC_KEY_INVALID_MSG
#  @brief Error message displayed if the selected public key file is invalid or corrupted.
PUBLIC_KEY_INVALID_MSG = "The selected file is not a valid public key or is corrupted. Please verify the key file."

## @var PDF_INVALID_MSG
#  @brief Error message displayed if the selected PDF file is invalid or cannot be read.
PDF_INVALID_MSG = "The selected file is not a valid PDF file. Please verify the PDF and try again."

## @var NO_SIGNATURE_MSG
#  @brief Message displayed if the selected PDF file does not contain a digital signature.
NO_SIGNATURE_MSG = "This PDF file does not appear to be signed. Please select a signed PDF."

## @var VERIFICATION_ERROR_MSG
#  @brief General error message displayed if an unexpected error occurs during verification.
VERIFICATION_ERROR_MSG = "An error occurred during verification. Please try again."

## @var SIGNATURE_VALID_MSG
#  @brief Message displayed in the status label when the PDF signature is successfully validated.
SIGNATURE_VALID_MSG = "The signature is VALID."

## @var SIGNATURE_INVALID_MSG
#  @brief Message displayed in the status label when the PDF signature is found to be invalid.
SIGNATURE_INVALID_MSG = "The signature is INVALID."

FOREGROUND_COLOR = "#ffffff"
BACKGROUND_COLOR = "#1e1e1e"
BACKGROUND2_COLOR = "#2d2d2d"
BLUE_BUTTON_COLOR = "#007acc"
ACTIVATE_BUTTON_COLOR = "#005f99"

## @class VerifyingFrame
#  @brief The VerifyingFrame class provides the UI for PDF signature verification.
#  @details This frame allows users to select a PDF file and a public key file.
#           It then attempts to verify the PDF's signature using the provided key
#           and displays the result (valid, invalid, or error messages).
#           Inherits from tk.Frame.
class VerifyingFrame(tk.Frame):
    ## @brief Initializes the VerifyingFrame.
    #  @param parent The parent tk.Tk window or tk.Frame that this frame will be placed in.
    #  @type parent tk.Tk
    #  @param end_verifying_callback A function to be called when the verification process is completed.
    #                                This callback should take no arguments and return None.
    #  @type end_verifying_callback Callable[[], None]
    def __init__(self, parent: tk.Tk, end_verifying_callback: Callable[[], None]):
        super().__init__(parent)

        self.end_verifying_callback = end_verifying_callback

        self.pdf_to_verify_path_var = tk.StringVar()
        self.public_key_path_var = tk.StringVar()

        self._setup_ui()

    ## @brief Sets up the user interface elements for the VerifyingFrame.
    #  @details This private method creates and arranges labels, entry fields for file paths,
    #           and buttons for file selection and initiating verification.
    def _setup_ui(self):
        self.configure(bg=BACKGROUND_COLOR)
        self.status_label = tk.Label(
            self,
            text=INITIAL_INSTRUCTION_TEXT,
            font=LARGE_FONT_CONFIG,
            wraplength=DEFAULT_WRAP_LENGTH,
            fg=FOREGROUND_COLOR,
            bg=BACKGROUND_COLOR,
        )
        self.status_label.pack(side=tk.TOP, fill=tk.X, padx=DEFAULT_PADDING_X, pady=(DEFAULT_PADDING_Y, SECTION_SPACING_Y))

        # --- PDF to Verify Selection ---
        pdf_selection_label = tk.Label(self, text="PDF file to verify:", fg=FOREGROUND_COLOR, bg=BACKGROUND_COLOR)
        pdf_selection_label.pack(anchor='center', padx=DEFAULT_PADDING_X, pady=(0, DEFAULT_PADDING_Y))

        self.pdf_to_verify_entry = tk.Entry(
            self,
            textvariable=self.pdf_to_verify_path_var,
            width=70,
            state="normal",
            fg=FOREGROUND_COLOR,
            bg=BACKGROUND2_COLOR,
            insertbackground="white"
        )
        self.pdf_to_verify_entry.pack(padx=DEFAULT_PADDING_X, pady=(0, DEFAULT_PADDING_Y), anchor="center")

        select_pdf_button = tk.Button(
            self,
            text="Select PDF file",
            command=self._select_pdf_to_verify_file,
            bg=BLUE_BUTTON_COLOR,
            fg="white",
            activebackground=ACTIVATE_BUTTON_COLOR
        )
        select_pdf_button.pack(padx=DEFAULT_PADDING_X, pady=(0, SECTION_SPACING_Y), anchor="center")

        # --- Public Key Selection ---
        public_key_label = tk.Label(self, text="Public key file:", fg=FOREGROUND_COLOR, bg=BACKGROUND_COLOR)
        public_key_label.pack(anchor='center', padx=DEFAULT_PADDING_X, pady=(0, DEFAULT_PADDING_Y))

        self.public_key_entry = tk.Entry(
            self,
            textvariable=self.public_key_path_var,
            width=70,
            state="normal",
            fg=FOREGROUND_COLOR,
            bg=BACKGROUND2_COLOR,
            insertbackground="white"
        )
        self.public_key_entry.pack(padx=DEFAULT_PADDING_X, pady=(0, DEFAULT_PADDING_Y), anchor="center")

        select_public_key_button = tk.Button(
            self,
            text="Select public key file",
            command=self._select_public_key_file,
            bg=BLUE_BUTTON_COLOR,
            fg="white",
            activebackground=ACTIVATE_BUTTON_COLOR
        )
        select_public_key_button.pack(padx=DEFAULT_PADDING_X, pady=(0, SECTION_SPACING_Y), anchor="center")

        # --- Verify Button ---
        self.verify_button = tk.Button(
            self,
            text=VERIFY_BUTTON_INITIAL_TEXT,
            command=self._process_verification,
            font=LARGE_FONT_CONFIG,
            bg=BLUE_BUTTON_COLOR,
            fg="white",
            activebackground=ACTIVATE_BUTTON_COLOR
        )
        self.verify_button.pack(side=tk.TOP, padx=DEFAULT_PADDING_X, pady=BUTTON_PADDING_Y)

    ## @brief Generic helper method to open a file dialog and update a Tkinter StringVar with the selected path.
    #  @param title The title for the file dialog window.
    #  @type title str
    #  @param file_types A list of tuples defining the acceptable file types for the dialog.
    #  @type file_types list
    #  @param string_var The tk.StringVar instance to update with the selected file path.
    #  @type string_var tk.StringVar
    def _select_file(self, title: str, file_types: list, string_var: tk.StringVar):
        """Helper to open a file dialog and update a StringVar."""
        file_path = filedialog.askopenfilename(title=title, filetypes=file_types)
        if file_path:
            string_var.set(file_path)

    ## @brief Opens a file dialog for the user to select the PDF file to be verified.
    #  @details Calls `_select_file` with appropriate parameters for PDF selection
    #           and updates `self.pdf_to_verify_path_var`.
    def _select_pdf_to_verify_file(self):
        self._select_file(SELECT_PDF_TO_VERIFY_TITLE, PDF_FILE_TYPES, self.pdf_to_verify_path_var)

    ## @brief Opens a file dialog for the user to select the public key file.
    #  @details Calls `_select_file` with appropriate parameters for public key selection
    #           and updates `self.public_key_path_var`.
    def _select_public_key_file(self):
        self._select_file(SELECT_PUBLIC_KEY_TITLE, PUBLIC_KEY_FILE_TYPES, self.public_key_path_var)

    ## @brief Helper method to update the status label and the main action button.
    #  @param status_message The message to display in the status label.
    #  @type status_message str
    #  @param button_text The new text for the action button.
    #  @type button_text str
    #  @param button_command The new command to associate with the action button.
    #                        Defaults to `_process_verification` if None.
    #  @type button_command Callable
    def _update_feedback(self, status_message: str, button_text: str, button_command: Callable = None):
        self.status_label.config(text=status_message)
        if button_command is None:
            button_command = self._process_verification
        self.verify_button.config(text=button_text, command=button_command)

    ## @brief Loads an RSA public key from a PEM-encoded file at the given path.
    #  @param path The file system path to the public key file.
    #  @type path str
    #  @return The loaded rsa.RSAPublicKey object if successful, otherwise None.
    #  @details If the file is not found or an error occurs during parsing, it updates
    #           the UI with an error message via `_update_feedback` and returns None.
    def _load_public_key(self, path: str) -> rsa.RSAPublicKey | None:
        try:
            with open(path, "rb") as f:
                public_key = serialization.load_pem_public_key(
                    f.read(),
                )
                return public_key
        except FileNotFoundError:
            self._update_feedback(PUBLIC_KEY_NOT_FOUND_MSG, VERIFY_BUTTON_RETRY_TEXT)
            return None
        except Exception:
            self._update_feedback(PUBLIC_KEY_INVALID_MSG, VERIFY_BUTTON_RETRY_TEXT)
            return None

    ## @brief Handles the PDF signature verification process.
    #  @details This method is called when the verify button is pressed.
    #           It retrieves the PDF and public key paths from the UI.
    #           Validates that both paths are provided.
    #           Loads the public key using `_load_public_key`.
    #           Calls `pdf_signer.verify` to perform the signature verification.
    #           Updates the UI with the result (valid, invalid) or an error message
    def _process_verification(self):
        pdf_path = self.pdf_to_verify_path_var.get()
        public_key_path = self.public_key_path_var.get()

        if not pdf_path or not public_key_path:
            self._update_feedback(PATHS_REQUIRED_MSG, VERIFY_BUTTON_RETRY_TEXT)
            return

        public_key = self._load_public_key(public_key_path)
        if public_key is None:
            return

        try:
            is_valid = pdf_signer.verify(public_key, pdf_path)
            if is_valid:
                self._update_feedback(SIGNATURE_VALID_MSG, VERIFY_BUTTON_GO_BACK_TEXT, self.end_verifying_callback)
            else:
                self._update_feedback(SIGNATURE_INVALID_MSG, VERIFY_BUTTON_GO_BACK_TEXT, self.end_verifying_callback)
        except PdfReadError:
            self._update_feedback(PDF_INVALID_MSG, VERIFY_BUTTON_RETRY_TEXT)
        except pdf_signer.NoSignatureFound:
            self._update_feedback(NO_SIGNATURE_MSG, VERIFY_BUTTON_RETRY_TEXT)
        except Exception as e:
            self._update_feedback(VERIFICATION_ERROR_MSG + f" (Details: {type(e).__name__})", VERIFY_BUTTON_RETRY_TEXT)
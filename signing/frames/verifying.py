"""
A Tkinter Frame for selecting a PDF file and a public key to verify the PDF's digital signature.
"""

import tkinter as tk
from tkinter import filedialog
from typing import Callable

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pyhanko.pdf_utils.misc import PdfReadError
from services import pdf_signer


LARGE_FONT_CONFIG = ("TkDefaultFont", 16)
DEFAULT_WRAP_LENGTH = 750
PDF_FILE_TYPES = [("PDF files", "*.pdf")]
PUBLIC_KEY_FILE_TYPES = [("Public Key files", "*.pem *.key")]

SELECT_PDF_TO_VERIFY_TITLE = "Select the PDF file to verify"
SELECT_PUBLIC_KEY_TITLE = "Select the public key file"

DEFAULT_PADDING_X = 10
DEFAULT_PADDING_Y = 10
SECTION_SPACING_Y = 20
BUTTON_PADDING_Y = 20

# Text constants
INITIAL_INSTRUCTION_TEXT = "Please choose the PDF file to verify and the public key corresponding to the signature."
VERIFY_BUTTON_INITIAL_TEXT = "Verify PDF Signature"
VERIFY_BUTTON_RETRY_TEXT = "Try Again"
VERIFY_BUTTON_GO_BACK_TEXT = "Go back to main menu"

# Error/Status Messages
PATHS_REQUIRED_MSG = "Both PDF file and public key file locations are required. Please select them."
PUBLIC_KEY_NOT_FOUND_MSG = "Public key file not found at the specified location. Please check the path and try again."
PUBLIC_KEY_INVALID_MSG = "The selected file is not a valid public key or is corrupted. Please verify the key file."
PDF_INVALID_MSG = "The selected file is not a valid PDF file. Please verify the PDF and try again."
NO_SIGNATURE_MSG = "This PDF file does not appear to be signed. Please select a signed PDF."
VERIFICATION_ERROR_MSG = "An error occurred during verification. Please try again."
SIGNATURE_VALID_MSG = "The signature is VALID."
SIGNATURE_INVALID_MSG = "The signature is INVALID."


class VerifyingFrame(tk.Frame):
    def __init__(self, parent: tk.Tk, end_verifying_callback: Callable[[], None]):
        super().__init__(parent)

        self.end_verifying_callback = end_verifying_callback

        self.pdf_to_verify_path_var = tk.StringVar()
        self.public_key_path_var = tk.StringVar()

        self._setup_ui()

    def _setup_ui(self):
        """Creates and arranges UI elements within the frame."""
        self.status_label = tk.Label(
            self,
            text=INITIAL_INSTRUCTION_TEXT,
            font=LARGE_FONT_CONFIG,
            wraplength=DEFAULT_WRAP_LENGTH,
        )
        self.status_label.pack(side=tk.TOP, fill=tk.X, padx=DEFAULT_PADDING_X, pady=(DEFAULT_PADDING_Y, SECTION_SPACING_Y))

        # --- PDF to Verify Selection ---
        pdf_selection_label = tk.Label(self, text="PDF file to verify:")
        pdf_selection_label.pack(anchor='center', padx=DEFAULT_PADDING_X, pady=(0, DEFAULT_PADDING_Y))

        self.pdf_to_verify_entry = tk.Entry(
            self,
            textvariable=self.pdf_to_verify_path_var,
            width=70,
            state="readonly"
        )
        self.pdf_to_verify_entry.pack(padx=DEFAULT_PADDING_X, pady=(0, DEFAULT_PADDING_Y), anchor="center")

        select_pdf_button = tk.Button(
            self,
            text="Select PDF file",
            command=self._select_pdf_to_verify_file
        )
        select_pdf_button.pack(padx=DEFAULT_PADDING_X, pady=(0, SECTION_SPACING_Y), anchor="center")

        # --- Public Key Selection ---
        public_key_label = tk.Label(self, text="Public key file:")
        public_key_label.pack(anchor='center', padx=DEFAULT_PADDING_X, pady=(0, DEFAULT_PADDING_Y))

        self.public_key_entry = tk.Entry(
            self,
            textvariable=self.public_key_path_var,
            width=70,
            state="readonly"
        )
        self.public_key_entry.pack(padx=DEFAULT_PADDING_X, pady=(0, DEFAULT_PADDING_Y), anchor="center")

        select_public_key_button = tk.Button(
            self,
            text="Select public key file",
            command=self._select_public_key_file
        )
        select_public_key_button.pack(padx=DEFAULT_PADDING_X, pady=(0, SECTION_SPACING_Y), anchor="center")

        # --- Verify Button ---
        self.verify_button = tk.Button(
            self,
            text=VERIFY_BUTTON_INITIAL_TEXT,
            command=self._process_verification,
            font=LARGE_FONT_CONFIG
        )
        self.verify_button.pack(side=tk.TOP, padx=DEFAULT_PADDING_X, pady=BUTTON_PADDING_Y)

    def _select_file(self, title: str, file_types: list, string_var: tk.StringVar):
        """Helper to open a file dialog and update a StringVar."""
        file_path = filedialog.askopenfilename(title=title, filetypes=file_types)
        if file_path:
            string_var.set(file_path)

    def _select_pdf_to_verify_file(self):
        self._select_file(SELECT_PDF_TO_VERIFY_TITLE, PDF_FILE_TYPES, self.pdf_to_verify_path_var)

    def _select_public_key_file(self):
        self._select_file(SELECT_PUBLIC_KEY_TITLE, PUBLIC_KEY_FILE_TYPES, self.public_key_path_var)

    def _update_feedback(self, status_message: str, button_text: str, button_command: Callable = None):
        """Helper to update status label and verify button."""
        self.status_label.config(text=status_message)
        if button_command is None:
            button_command = self._process_verification
        self.verify_button.config(text=button_text, command=button_command)

    def _load_public_key(self, path: str) -> rsa.RSAPublicKey | None:
        """Loads a public key from the given path."""
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


    def _process_verification(self):
        """Handles the PDF signature verification process."""
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
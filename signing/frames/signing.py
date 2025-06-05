"""
A Tkinter Frame for selecting a PDF, choosing an output location, and signing the PDF.
"""

import tkinter as tk
from tkinter import filedialog
from typing import Callable

from cryptography.hazmat.primitives.asymmetric import rsa
from pyhanko.pdf_utils.misc import PdfReadError
from pyhanko.sign.general import SigningError
from services import pdf_signer

# UI Configuration Constants
LARGE_FONT_CONFIG = ("TkDefaultFont", 16)
DEFAULT_WRAP_LENGTH = 750
PDF_FILE_TYPES = [("PDF files", "*.pdf")]

# Dialog Title Constants
SELECT_SOURCE_PDF_TITLE = "Select the PDF file to sign"
SELECT_TARGET_PDF_TITLE = "Set target location and filename for signed PDF"

# Label Text Constants
INITIAL_STATUS_TEXT = "Please choose the PDF file to sign and where the signed PDF file should be placed."
SOURCE_PDF_LABEL_TEXT = "Selected PDF file to sign:"
TARGET_PDF_LABEL_TEXT = "Location where the signed PDF file will be saved:"

# Button Text Constants
SELECT_SOURCE_BUTTON_TEXT = "Select PDF file"
SELECT_TARGET_BUTTON_TEXT = "Set target location"
SIGN_BUTTON_INITIAL_TEXT = "Sign the PDF file"
RETRY_BUTTON_TEXT = "Try Again"
GO_BACK_BUTTON_TEXT = "Go back to main menu"

# Status/Error Message Constants
PATHS_REQUIRED_ERROR_TEXT = "Both original and target PDF locations are required. Please select them."
SIGNING_SUCCESS_TEXT = "Successfully signed PDF and saved to the designated location."
PDF_READ_ERROR_TEXT = " selected source file is not a valid PDF file. Please verify and try again."
SIGNING_ERROR_TEXT = "This PDF file may have already been signed or is unsuitable for signing. Please choose a different file."
UNEXPECTED_SIGNING_ERROR_TEXT = "An unexpected error occurred during signing: {error_type}. Please try again"

FOREGROUND_COLOR = "#ffffff"
BACKGROUND_COLOR = "#1e1e1e"
BACKGROUND2_COLOR = "#2d2d2d"
BLUE_BUTTON_COLOR = "#007acc"
ACTIVATE_BUTTON_COLOR = "#005f99"

class SigningFrame(tk.Frame):
    def __init__(self, parent: tk.Tk, private_key: rsa.RSAPrivateKey, end_signing_callback: Callable[[], None]):
        super().__init__(parent)

        self.private_key = private_key
        self.end_signing_callback = end_signing_callback

        self.source_pdf_path_var = tk.StringVar()
        self.target_pdf_path_var = tk.StringVar()

        self._setup_ui()

    def _setup_ui(self):
        self.configure(bg=BACKGROUND_COLOR)

        self.status_label = tk.Label(
            self,
            text=INITIAL_STATUS_TEXT,
            font=LARGE_FONT_CONFIG,
            wraplength=DEFAULT_WRAP_LENGTH,
            fg=FOREGROUND_COLOR,
            bg=BACKGROUND_COLOR
        )
        """Creates and arranges UI elements within the frame."""
        self.status_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # --- Source PDF Selection ---
        source_pdf_label = tk.Label(self, text=SOURCE_PDF_LABEL_TEXT, fg=FOREGROUND_COLOR, bg=BACKGROUND_COLOR)
        source_pdf_label.pack(anchor='center', padx=5, pady=(10, 0))

        self.source_pdf_path_entry = tk.Entry(
            self,
            textvariable=self.source_pdf_path_var,
            width=70,
            state="normal",
            fg = FOREGROUND_COLOR,
            bg = BACKGROUND2_COLOR,
            insertbackground = "white"
        )
        self.source_pdf_path_entry.pack(padx=10, pady=(0, 5), anchor="center")

        select_source_pdf_button = tk.Button(
            self,
            text=SELECT_SOURCE_BUTTON_TEXT,
            command=self._select_source_pdf_file,
            bg=BLUE_BUTTON_COLOR,
            fg="white",
            activebackground=ACTIVATE_BUTTON_COLOR
        )
        select_source_pdf_button.pack(padx=10, pady=(0, 20), anchor="center")

        # --- Target PDF Selection ---
        target_pdf_label = tk.Label(self, text=TARGET_PDF_LABEL_TEXT, fg=FOREGROUND_COLOR, bg=BACKGROUND_COLOR)
        target_pdf_label.pack(anchor='center', padx=5, pady=(10, 0))

        self.target_pdf_path_entry = tk.Entry(
            self,
            textvariable=self.target_pdf_path_var,
            width=70,
            state="normal",
            fg=FOREGROUND_COLOR,
            bg=BACKGROUND2_COLOR,
            insertbackground="white"
        )
        self.target_pdf_path_entry.pack(padx=10, pady=(0, 5), anchor="center")

        select_target_pdf_button = tk.Button(
            self,
            text=SELECT_TARGET_BUTTON_TEXT,
            command=self._select_target_pdf_path,
            bg=BLUE_BUTTON_COLOR,
            fg="white",
            activebackground=ACTIVATE_BUTTON_COLOR
        )
        select_target_pdf_button.pack(padx=10, pady=(0, 20), anchor="center")

        # --- Sign Button ---
        self.sign_button = tk.Button(
            self,
            text=SIGN_BUTTON_INITIAL_TEXT,
            command=self._sign_pdf_document,
            font=LARGE_FONT_CONFIG,
            bg=BLUE_BUTTON_COLOR,
            fg="white",
            activebackground=ACTIVATE_BUTTON_COLOR
        )
        self.sign_button.pack(side=tk.TOP, padx=10, pady=20)


    def _select_source_pdf_file(self):
        """Opens a dialog to select the source PDF file and updates the corresponding Entry."""
        file_path = filedialog.askopenfilename(
            title=SELECT_SOURCE_PDF_TITLE,
            filetypes=PDF_FILE_TYPES
        )
        if file_path:
            self.source_pdf_path_var.set(file_path)

    def _select_target_pdf_path(self):
        """Opens a dialog to select the target PDF file path and updates the corresponding Entry."""
        file_path = filedialog.asksaveasfilename(
            title=SELECT_TARGET_PDF_TITLE,
            filetypes=PDF_FILE_TYPES,
            defaultextension=".pdf" # Suggest .pdf extension
        )
        if file_path:
            self.target_pdf_path_var.set(file_path)

    def _update_feedback(self, status_message: str, button_text: str, button_command: Callable = None):
        """Helper to update status label and sign button."""
        self.status_label.config(text=status_message)
        if button_command is None:
            button_command = self._sign_pdf_document
        self.sign_button.config(text=button_text, command=button_command)

    def _sign_pdf_document(self):
        """Handles the PDF signing process and UI feedback."""
        source_pdf_path = self.source_pdf_path_var.get()
        target_pdf_path = self.target_pdf_path_var.get()

        if not source_pdf_path or not target_pdf_path:
            self._update_feedback(
                PATHS_REQUIRED_ERROR_TEXT,
                RETRY_BUTTON_TEXT
            )
            return

        try:
            pdf_signer.sign(self.private_key, source_pdf_path, target_pdf_path)
            self._update_feedback(SIGNING_SUCCESS_TEXT, GO_BACK_BUTTON_TEXT, self.end_signing_callback)
        except PdfReadError:
            self._update_feedback(PDF_READ_ERROR_TEXT, RETRY_BUTTON_TEXT)
        except SigningError:
            self._update_feedback(SIGNING_ERROR_TEXT, RETRY_BUTTON_TEXT)
        except Exception as e:
            self._update_feedback(UNEXPECTED_SIGNING_ERROR_TEXT.format(error_type=type(e).__name__),RETRY_BUTTON_TEXT)
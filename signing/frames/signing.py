## @file signing.py
#  @brief A Tkinter Frame for selecting a PDF, choosing an output location, and signing the PDF.
#  @details This frame guides the user through selecting an input PDF, specifying an output path
#           for the signed PDF, and then performs the signing operation using a provided private key.
#           It handles UI updates for status messages and error reporting.

import tkinter as tk
from tkinter import filedialog
from typing import Callable

from cryptography.hazmat.primitives.asymmetric import rsa
from pyhanko.pdf_utils.misc import PdfReadError
from pyhanko.sign.general import SigningError
from services import pdf_signer

## @var LARGE_FONT_CONFIG
#  @brief Font configuration for large text elements (e.g., status labels, buttons).
LARGE_FONT_CONFIG = ("TkDefaultFont", 16)

## @var DEFAULT_WRAP_LENGTH
#  @brief Default wrap length in pixels for text in labels to ensure proper layout.
DEFAULT_WRAP_LENGTH = 750

## @var PDF_FILE_TYPES
#  @brief File type filter used in file dialogs, restricting selection to PDF files.
PDF_FILE_TYPES = [("PDF files", "*.pdf")]

## @var SELECT_SOURCE_PDF_TITLE
#  @brief Title for the file dialog when selecting the source PDF to be signed.
SELECT_SOURCE_PDF_TITLE = "Select the PDF file to sign"

## @var SELECT_TARGET_PDF_TITLE
#  @brief Title for the file dialog when selecting the output path for the signed PDF.
SELECT_TARGET_PDF_TITLE = "Set target location and filename for signed PDF"

## @var INITIAL_STATUS_TEXT
#  @brief Initial instructional text displayed in the status label.
INITIAL_STATUS_TEXT = "Please choose the PDF file to sign and where the signed PDF file should be placed."

## @var SOURCE_PDF_LABEL_TEXT
#  @brief Text for the label indicating the selected source PDF file path.
SOURCE_PDF_LABEL_TEXT = "Selected PDF file to sign:"

## @var TARGET_PDF_LABEL_TEXT
#  @brief Text for the label indicating the selected target path for the signed PDF file.
TARGET_PDF_LABEL_TEXT = "Location where the signed PDF file will be saved:"

## @var SELECT_SOURCE_BUTTON_TEXT
#  @brief Text for the button used to trigger source PDF file selection.
SELECT_SOURCE_BUTTON_TEXT = "Select PDF file"

## @var SELECT_TARGET_BUTTON_TEXT
#  @brief Text for the button used to trigger target PDF path selection.
SELECT_TARGET_BUTTON_TEXT = "Set target location"

## @var SIGN_BUTTON_INITIAL_TEXT
#  @brief Initial text for the button that initiates the PDF signing process.
SIGN_BUTTON_INITIAL_TEXT = "Sign the PDF file"

## @var RETRY_BUTTON_TEXT
#  @brief Text for the main action button when a retry is suggested after an error.
RETRY_BUTTON_TEXT = "Try Again"

## @var GO_BACK_BUTTON_TEXT
#  @brief Text for the main action button to navigate back to the main menu after success.
GO_BACK_BUTTON_TEXT = "Go back to main menu"

## @var PATHS_REQUIRED_ERROR_TEXT
#  @brief Error message displayed when either source or target PDF paths are not selected.
PATHS_REQUIRED_ERROR_TEXT = "Both original and target PDF locations are required. Please select them."

## @var PATHS_CANNOT_BE_THE_SAME_ERROR_TEXT
#  @brief Error message displayed when source or target PDF paths are the same.
PATHS_CANNOT_BE_THE_SAME_ERROR_TEXT = "Original and target PDF locations cannot be the same. Please change one of them and try again."

## @var SIGNING_SUCCESS_TEXT
#  @brief Message displayed in the status label upon successful PDF signing.
SIGNING_SUCCESS_TEXT = "Successfully signed PDF and saved to the designated location."

## @var PDF_READ_ERROR_TEXT
#  @brief Error message displayed if the selected source file is not a valid PDF.
PDF_READ_ERROR_TEXT = "Selected source file is not a valid PDF file. Please verify and try again." # Note: Original text has a leading space.

## @var SIGNING_ERROR_TEXT
#  @brief Error message displayed if the PDF is already signed or unsuitable for signing.
SIGNING_ERROR_TEXT = "This PDF file may have already been signed or is unsuitable for signing. Please choose a different file."

## @var UNEXPECTED_SIGNING_ERROR_TEXT
#  @brief Error message template for unexpected errors during the signing process.
UNEXPECTED_SIGNING_ERROR_TEXT = "An unexpected error occurred during signing: {error_type}. Please try again"


## @brief The SigningFrame class provides the UI for the PDF signing process.
#  @details This frame allows users to select a source PDF, specify a target location for the signed PDF,
#           and initiate the signing operation. It handles user interactions and feedback.
#           Inherits from tk.Frame.
class SigningFrame(tk.Frame):
    ## @brief Initializes the SigningFrame.
    #  @param parent The parent tk.Tk window or tk.Frame that this frame will be placed in.
    #  @type parent tk.Tk
    #  @param private_key The RSA private key to be used for signing the PDF document.
    #  @type private_key rsa.RSAPrivateKey
    #  @param end_signing_callback A function to be called when the signing process is completed (either successfully or to go back).
    #                              This callback should take no arguments and return None.
    #  @type end_signing_callback Callable[[], None]
    def __init__(self, parent: tk.Tk, private_key: rsa.RSAPrivateKey, end_signing_callback: Callable[[], None]):
        super().__init__(parent)

        self.private_key = private_key
        self.end_signing_callback = end_signing_callback

        self.source_pdf_path_var = tk.StringVar()
        self.target_pdf_path_var = tk.StringVar()

        self._setup_ui()

    ## @brief Sets up the user interface elements for the SigningFrame.
    #  @details This private method creates and arranges labels, entry fields for paths,
    #           and buttons for file selection and signing.
    def _setup_ui(self):
        self.status_label = tk.Label(
            self,
            text=INITIAL_STATUS_TEXT,
            font=LARGE_FONT_CONFIG,
            wraplength=DEFAULT_WRAP_LENGTH,
        )
        self.status_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # --- Source PDF Selection ---
        source_pdf_label = tk.Label(self, text=SOURCE_PDF_LABEL_TEXT)
        source_pdf_label.pack(anchor='center', padx=5, pady=(10, 0))

        self.source_pdf_path_entry = tk.Entry(
            self,
            textvariable=self.source_pdf_path_var,
            width=70,
            state="readonly"
        )
        self.source_pdf_path_entry.pack(padx=10, pady=(0, 5), anchor="center")

        select_source_pdf_button = tk.Button(
            self,
            text=SELECT_SOURCE_BUTTON_TEXT,
            command=self._select_source_pdf_file
        )
        select_source_pdf_button.pack(padx=10, pady=(0, 20), anchor="center")

        # --- Target PDF Selection ---
        target_pdf_label = tk.Label(self, text=TARGET_PDF_LABEL_TEXT)
        target_pdf_label.pack(anchor='center', padx=5, pady=(10, 0))

        self.target_pdf_path_entry = tk.Entry(
            self,
            textvariable=self.target_pdf_path_var,
            width=70,
            state="readonly"
        )
        self.target_pdf_path_entry.pack(padx=10, pady=(0, 5), anchor="center")

        select_target_pdf_button = tk.Button(
            self,
            text=SELECT_TARGET_BUTTON_TEXT,
            command=self._select_target_pdf_path
        )
        select_target_pdf_button.pack(padx=10, pady=(0, 20), anchor="center")

        # --- Sign Button ---
        self.sign_button = tk.Button(
            self,
            text=SIGN_BUTTON_INITIAL_TEXT,
            command=self._sign_pdf_document,
            font=LARGE_FONT_CONFIG
        )
        self.sign_button.pack(side=tk.TOP, padx=10, pady=20)

    ## @brief Opens a file dialog to allow the user to select the source PDF file.
    #  @details Updates the `source_pdf_path_var` and the corresponding entry field
    #           with the path of the file selected by the user.
    def _select_source_pdf_file(self):
        file_path = filedialog.askopenfilename(
            title=SELECT_SOURCE_PDF_TITLE,
            filetypes=PDF_FILE_TYPES
        )
        if file_path:
            self.source_pdf_path_var.set(file_path)

    ## @brief Opens a file dialog to allow the user to select the target path and filename for the signed PDF.
    #  @details Updates the `target_pdf_path_var` and the corresponding entry field
    #           with the path chosen by the user. Suggests ".pdf" as the default extension.
    def _select_target_pdf_path(self):
        file_path = filedialog.asksaveasfilename(
            title=SELECT_TARGET_PDF_TITLE,
            filetypes=PDF_FILE_TYPES,
            defaultextension=".pdf" # Suggest .pdf extension
        )
        if file_path:
            self.target_pdf_path_var.set(file_path)

    ## @brief Helper method to update the status label and the main action button's text and command.
    #  @param status_message The message to display in the status label.
    #  @type status_message str
    #  @param button_text The new text for the action.
    #  @type button_text str
    #  @param button_command The new command to associate with the action button.
    #                        Defaults to `_sign_pdf_document` if None.
    #  @type button_command Callable
    def _update_feedback(self, status_message: str, button_text: str, button_command: Callable = None):
        """Helper to update status label and sign button."""
        self.status_label.config(text=status_message)
        if button_command is None:
            button_command = self._sign_pdf_document
        self.sign_button.config(text=button_text, command=button_command)

    ## @brief Handles the PDF signing process based on selected file paths and the provided private key.
    #  @details This method is called when the sign button is pressed.
    #           It validates that both source and target paths are provided and are not the same.
    #           It then attempts to sign the PDF using `pdf_signer.sign` and
    #           updates the UI with success or error messages via `_update_feedback`.
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

        if source_pdf_path == target_pdf_path:
            self._update_feedback(
                PATHS_CANNOT_BE_THE_SAME_ERROR_TEXT,
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
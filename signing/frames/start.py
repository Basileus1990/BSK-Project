## @file start.py
#  @brief A Tkinter Frame providing options to navigate to PDF signing or verification sections.
#  @details This frame serves as the initial screen, allowing users to choose between
#           the signing workflow or the verification workflow.

import tkinter as tk
from typing import Callable

## @var LARGE_FONT_CONFIG
#  @brief Font configuration for large text elements.
#  @details Tuple specifying font family ("TkDefaultFont") and size (16).
LARGE_FONT_CONFIG = ("TkDefaultFont", 16)

## @var DEFAULT_WRAP_LENGTH
#  @brief Default wrap length in pixels for text in labels.
#  @details Used to ensure text fits within the UI layout.
DEFAULT_WRAP_LENGTH = 750

## @var DEFAULT_PADDING_X
#  @brief Default horizontal padding in pixels for UI elements.
DEFAULT_PADDING_X = 200

## @var DEFAULT_PADDING_Y
#  @brief Default vertical padding in pixels for general UI elements.
DEFAULT_PADDING_Y = 10

## @var BUTTON_PADDING_Y
#  @brief Specific vertical padding in pixels for buttons.
BUTTON_PADDING_Y = 20

## @var LABEL_TEXT
#  @brief Text content for the main instruction label on the StartFrame.
LABEL_TEXT = "Please choose whether you want to sign a PDF or verify the signature of a PDF file."

## @var SIGN_BUTTON_TEXT
#  @brief Text content for the button that initiates the PDF signing process.
SIGN_BUTTON_TEXT = "Sign a PDF file"

## @var VERIFY_BUTTON_TEXT
#  @brief Text content for the button that initiates the PDF signature verification process.
VERIFY_BUTTON_TEXT = "Verify PDF file signature"


## @class StartFrame
#  @brief The StartFrame class provides user interface for the application.
#  @details This frame displays options for the user to either start the PDF signing
#           process or the PDF signature verification process. It inherits from tk.Frame.
class StartFrame(tk.Frame):
    ## @brief Initializes the StartFrame.
    #  @param parent The parent tk.Tk window or tk.Frame that this frame will be placed in.
    #  @type parent tk.Tk
    #  @param on_signing_chosen_callback A function to be called when the user chooses to sign a PDF.
    #                                    This callback should take no arguments and return None.
    #  @type on_signing_chosen_callback Callable[[], None]
    #  @param on_verifying_chosen_callback A function to be called when the user chooses to verify a PDF signature.
    #                                      This callback should take no arguments and return None.
    #  @type on_verifying_chosen_callback Callable[[], None]
    def __init__(self, parent: tk.Tk, on_signing_chosen_callback: Callable[[], None], on_verifying_chosen_callback: Callable[[], None]):
        super().__init__(parent)

        self.on_signing_chosen_callback = on_signing_chosen_callback
        self.on_verifying_chosen_callback = on_verifying_chosen_callback

        self._setup_ui()

    ## @brief Sets up the user interface elements for the StartFrame.
    #  @details This private method creates and arranges the instruction label and
    #           the sign and verify buttons within the frame.
    def _setup_ui(self):
        instruction_label = tk.Label(
            self,
            text=LABEL_TEXT,
            font=LARGE_FONT_CONFIG,
            wraplength=DEFAULT_WRAP_LENGTH,
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
            font=LARGE_FONT_CONFIG
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
            font=LARGE_FONT_CONFIG
        )
        verify_button.pack(
            side=tk.TOP,
            padx=DEFAULT_PADDING_X,
            pady=BUTTON_PADDING_Y,
            fill=tk.X
        )
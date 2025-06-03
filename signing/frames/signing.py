"""
This frame is the view for checking for usb drive and reading the key from it
"""

import tkinter as tk
from tkinter import filedialog

from cryptography.hazmat.primitives.asymmetric import rsa
from services import pdf_signer
from typing import Callable


class SigningFrame(tk.Frame):
    def __init__(self, parent: tk.Tk, key: rsa.RSAPrivateKey):
        tk.Frame.__init__(self, parent)

        self.key = key

        self.label = tk.Label(
            self,
            text="Please choose the PDF file to sign and where the signed PDF file should be placed",
            font=("TkDefaultFont", 16),
            wraplength=750,
        )
        self.label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Original PDF selection
        self.label_pdf_selection = tk.Label(self, text="Selected PDF file")
        self.label_pdf_selection.pack(anchor='center', padx=5)
        self.pdf_localization = tk.Entry(self, width=50, state="readonly")
        self.pdf_localization.pack(padx=5, pady=(0, 10), anchor="center")
        self.button_pdf_selection = tk.Button(
            self,
            text="Select PDF file",
            command=lambda: self.select_PDF_file(self.pdf_localization))
        self.button_pdf_selection.pack(padx=5, pady=(0, 10), anchor="center")

        # Target PDF selection
        self.pdf_target_pdf_selection = tk.Label(self, text="Localisation where the signed PDF file will be saved:")
        self.pdf_target_pdf_selection.pack(anchor='center', padx=5)
        self.target_pdf_localization = tk.Entry(self, width=50, state="readonly")
        self.target_pdf_localization.pack(padx=5, pady=(0, 10), anchor="center")
        self.button_target_pdf_selection = tk.Button(
            self,
            text="Set target localization",
            command=lambda: self.select_target_PDF_localisation_and_name(self.target_pdf_localization))
        self.button_target_pdf_selection.pack(padx=5, pady=(0, 10), anchor="center")


        self.button = tk.Button(
            self,
            text="Sign the PDF file",
            command=self.sign_pdf,
            font=("TkDefaultFont", 16)
        )
        self.button.pack(side=tk.TOP, padx=5, pady=5)

    def select_PDF_file(self, entry):
        folder = filedialog.askopenfilename(title="Select a public key", filetypes=[("PDF files", "*.pdf")])

        if folder:
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, folder)
            entry.config(state='readonly')

    def select_target_PDF_localisation_and_name(self, entry):
        folder = filedialog.asksaveasfilename(title="Select a public key", filetypes=[("PDF files", "*.pdf")])

        if folder:
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, folder)
            entry.config(state='readonly')


    def sign_pdf(self):
        pdf_localization = self.pdf_localization.get()
        target_pdf_localization = self.target_pdf_localization.get()

        if not pdf_localization or not target_pdf_localization:
            self.label['text'] = "Both original and target localizations are required. Please select them and try again"
            self.button['text'] = "Try Again"
            return

        try:
            pdf_signer.sign(self.key, pdf_localization, target_pdf_localization)
        except Exception as e:
            self.label['text'] = str(e)
            self.button['text'] = "Try Again"
            return

        self.label['text'] = "Successfully signed PDF at designated location"

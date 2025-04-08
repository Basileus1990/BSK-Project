"""
This package is responsible for signing and verifying the pdf file using the private/public key
"""

from PyPDF2 import PdfReader, PdfWriter


def sign(private_key: str, pdf_path: str):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    writer.append_pages_from_reader(reader)
    writer.add_metadata(reader.metadata)

    # Write your custom metadata here:
    writer.add_metadata({"/test": "this"})

    with open("your_original.pdf", "ab") as fout:
        # ab is append binary; if you do wb, the file will append blank pages
        writer.write(fout)



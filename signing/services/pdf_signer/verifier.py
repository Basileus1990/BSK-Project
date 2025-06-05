## @file verifier.py
#  @brief Provides functionality to verify digital signatures in PDF documents.
#  @details This module uses `pyhanko` and `cryptography` libraries to validate
#           the integrity of a PDF signature and compare the embedded public key
#           with a provided public key.

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import load_der_x509_certificate

from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature
from pyhanko_certvalidator import ValidationContext

## @brief Exception raised when a PDF document does not contain any embedded digital signatures.
class NoSignatureFound(Exception):
    pass


## @brief Verifies the digital signature found in a PDF document against a provided public key.
#  @details This function reads a PDF, extracts its first embedded signature, and performs two main checks:
#           1. It compares the public key embedded in the signature's certificate with the `public_key` argument.
#              If they do not match, verification fails (returns `False`).
#           2. It validates the integrity of the signature itself using `pyhanko`'s validation mechanism.
#              For self-signed certificates, it creates a `ValidationContext`
#              trusting the embedded certificate itself to validate the signature.
#  @param public_key The RSA public key expected to correspond to the signature.
#  @type public_key rsa.RSAPublicKey
#  @param pdf_path The file system path to the PDF document whose signature is to be verified.
#  @type pdf_path str
#  @return `True` if the embedded public key matches the provided `public_key` AND the signature is intact
#          Returns `False` otherwise.
#  @rtype bool
#  @exception FileNotFoundError If the `pdf_path` does not exist.
#  @exception NoSignatureFound If the PDF document does not contain any embedded signatures.
#  @exception PdfReadError When an error occurs during verifying or while reading the PDF file
def verify(public_key: rsa.RSAPublicKey, pdf_path: str) -> bool:
    with open(pdf_path, "rb") as inf:
        reader = PdfFileReader(inf, strict=False)

        signatures = reader.embedded_signatures
        if not signatures:
            raise NoSignatureFound

        sig = signatures[0]

        # Getting the certificate and its public key from the signature:
        asn1_cert = sig.signer_cert
        cert_bytes = asn1_cert.dump()
        crypto_cert = load_der_x509_certificate(cert_bytes, default_backend())

        # Comparing the signature public key to the one the user provided:
        embedded_pub = crypto_cert.public_key()
        if embedded_pub.public_numbers() != public_key.public_numbers():
            return False

        # Creating a trust root where our certificate is the root, so we can validate the self-signed certificate signature.
        vc = ValidationContext(trust_roots=[asn1_cert])
        status = validate_pdf_signature(sig, vc)


        if status.intact:
            return True
        else:
            return False

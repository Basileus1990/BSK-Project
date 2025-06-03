from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import load_der_x509_certificate

from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature
from pyhanko_certvalidator import ValidationContext

class NoSignatureFound(Exception):
    pass

# TODO: More error handling


def verify(public_key: rsa.RSAPublicKey, pdf_path: str) -> bool:
    """
    Verifies a PDF signature using a public key.
    """
    try:
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

    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise e
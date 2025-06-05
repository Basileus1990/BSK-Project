"""
This package is responsible for signing and verifying the pdf file using the private/public key
"""

import datetime
import os
from typing import Tuple

from cryptography import x509
from cryptography.hazmat._oid import ExtendedKeyUsageOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from asn1crypto import x509 as asn1_x509, keys as asn1_keys

from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers, PdfSignatureMetadata, PdfSigner
from pyhanko.sign.fields import SigFieldSpec
from pyhanko.sign.general import SigningError, UnacceptableSignerError
from pyhanko.sign.timestamps import DummyTimeStamper
from pyhanko_certvalidator.registry import SimpleCertificateStore


def sign(private_key: rsa.RSAPrivateKey, pdf_in_path: str, pdf_out_path: str):
    """
        Signs a PDF document in a PAdES-like manner using an RSA private key string.
        A self-signed certificate is generated on-the-fly for this purpose.

        Args:
            private_key: The RSA private key in PEM format as a string.
                                 It is assumed to be unencrypted.
            pdf_in_path: Path to the input PDF file.
            pdf_out_path: Path where the signed PDF file will be saved.
        """

    asn1_cert, asn1_private_key = _generate_self_signed_cert(private_key)

    certification_store = SimpleCertificateStore()
    certification_store.register(asn1_cert)

    signer = signers.SimpleSigner(
        signing_cert=asn1_cert,
        signing_key=asn1_private_key,
        cert_registry=certification_store,
    )

    timestamper = DummyTimeStamper(asn1_cert, asn1_private_key)

    field_name = 'PAdES-signature'
    sign_metadata = PdfSignatureMetadata(
        field_name=field_name,
    )
    sig_spec = SigFieldSpec(
        sig_field_name=field_name,
        on_page=0,
        box=(50, 775, 250, 830)
    )

    try:
        with open(pdf_in_path, "rb") as inf, open(pdf_out_path, "wb") as outf:
            writer = IncrementalPdfFileWriter(inf, strict=False)

            pdf_signer = PdfSigner(
                sign_metadata,
                signer,
                timestamper=timestamper,
                new_field_spec=sig_spec
            )
            pdf_signer.sign_pdf(writer, output=outf)
    except Exception as e:
        if os.path.exists(pdf_out_path):
            os.remove(pdf_out_path)
        raise e

    return True



def _generate_self_signed_cert(private_key: rsa.RSAPrivateKey) -> Tuple[asn1_x509.Certificate, asn1_keys.PrivateKeyInfo]:
    """
    Generates a self-signed certificate from an RSA private key object.
    Returns the certificate and the private key info in asn1crypto format (expected by pyhanko).
    """

    common_name = "myPAdESCertificate"
    public_key = private_key.public_key()

    builder = (
        x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)]))
        .issuer_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])) # Self-signed
        .public_key(public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3650)) # Valid for 10 years
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=True,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).
        add_extension(
            x509.ExtendedKeyUsage([
                ExtendedKeyUsageOID.CODE_SIGNING,
                ExtendedKeyUsageOID.TIME_STAMPING,
            ]),
            critical=False,
        )
    )

    cert = builder.sign(private_key, hashes.SHA256())

    # Converting to asn1crypto format
    der_cert = cert.public_bytes(serialization.Encoding.DER)
    asn1_cert = asn1_x509.Certificate.load(der_cert)

    key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    asn1_private_key = asn1_keys.PrivateKeyInfo.load(key_bytes)

    return asn1_cert, asn1_private_key
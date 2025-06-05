## @file signer.py
#  @brief Provides functions for signing PDF documents using RSA private keys.
#  @details This module leverages the `pyhanko` library to perform PAdES
#           digital signatures. It includes functionality to generate a self-signed
#           certificate on-the-fly for the signing process.

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
from pyhanko.sign.timestamps import DummyTimeStamper
from pyhanko_certvalidator.registry import SimpleCertificateStore


## @brief Signs a PDF document using a provided RSA private key.
#  @details This function creates a self-signed certificate from the given private key
#           and uses it to apply a digital signature to the input PDF. The signed
#           PDF is saved to the specified output path. A signature field is added
#           to the first page of the PDF. If an error occurs during signing,
#           any partially created output file is removed.
#  @param private_key The RSA private key object to use for signing.
#  @type private_key rsa.RSAPrivateKey
#  @param pdf_in_path The file system path to the input PDF document that needs to be signed.
#  @type pdf_in_path str
#  @param pdf_out_path The file system path where the signed PDF document will be saved.
#  @type pdf_out_path str
#  @exception FileNotFoundError When the input file doesn't exist
#  @exception PdfReadError When an error occurs during signature or while reading the input PDF file
def sign(private_key: rsa.RSAPrivateKey, pdf_in_path: str, pdf_out_path: str):
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


## @brief Generates a self-signed X.509 certificate and private key information in ASN.1 format.
#  @details This internal helper function takes an RSA private key and creates a
#           self-signed certificate suitable for use with `pyhanko`. The certificate
#           has a common name "myPAdESCertificate" and is valid for 10 years.
#  @param private_key The RSA private key object from which to generate the public key for the certificate
#                     and to sign the certificate.
#  @type private_key rsa.RSAPrivateKey
#  @return A tuple containing:
#          - `asn1_cert`: The generated self-signed certificate in `asn1crypto.x509.Certificate` format.
#          - `asn1_private_key`: The private key information in `asn1crypto.keys.PrivateKeyInfo` format.
#  @rtype Tuple[asn1_x509.Certificate, asn1_keys.PrivateKeyInfo]
#  @private
def _generate_self_signed_cert(private_key: rsa.RSAPrivateKey) -> Tuple[asn1_x509.Certificate, asn1_keys.PrivateKeyInfo]:
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
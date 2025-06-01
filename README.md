# Bezpieczeństwa Systemów Komputerowych Project

## TODO
- [ ] The GUI interface must allow to select any document (*.pdf) that will be signed.
- [x] The signature must use the RSA algorithm with a 4096-length key.
- [x] A pseudorandom generator must be used to generate the RSA keys.
- [x] The private key stored on the pendrive must be encrypted by the AES algorithm,
where the 256-bit key is the hash from PIN known only to user A.
- [x] Pendrive usage for storing the private RSA key is obligatory. The pendrive must
be detected and the encrypted RSA key automatically loaded to the main
application.
- [x] The public key can be stored on the hard disk of the computer or be transferred
to another physical computer to verify the signature.
- [ ] It is obligatory to implement status/message icons to present the state of the
application (recognition of hardware tool, reading the private key, signature
status).
- [x] It is assumed that only user A can sign the documents, there is no need to create
keys for two or more users.
- [x] It is allowed to use the available implementations / libraries of the AES, RSA,
SHA algorithms.
- [x] Any language can be used to develop the application.
- [ ] In the report, a brief description of performed tests must be included (e.g.
signing scenarios, signature verification, encryption/decryption of other files).
- [ ] In the report the code of the application must be partially included in a form of
listings, pointing out the main functions of the application. It is strongly advised
to provide a short and substantive description.
- [ ] The full code documentation must be created using Doxygen documentation
generator.
- [x] It is obligatory to include the applications code in GitHub repository and provide
the link in the final report.
- [ ] Application functionality must be presented during project submission.
